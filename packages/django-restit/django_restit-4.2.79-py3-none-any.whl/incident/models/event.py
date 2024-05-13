from django.db import models

from rest import models as rm
from rest.extra import JSONMetaData
from rest import log
from rest import settings
from objict import objict

import metrics

from datetime import datetime, timedelta
from .incident import Incident, INCIDENT_STATE_PENDING
from .rules import Rule

INCIDENT_METRICS = settings.get("INCIDENT_METRICS", False)
INCIDENT_EVENT_METRICS = settings.get("INCIDENT_EVENT_METRICS", False)
EVENT_TO_INCIDENT_LEVEL = settings.get("EVENT_TO_INCIDENT_LEVEL", 4)
EVENT_DETAIL_TEMPLATES = settings.get("EVENT_DETAIL_TEMPLATES", None)
EVENT_META_KEYWORDS = settings.get("EVENT_META_KEYWORDS", [
        "path", "ip", "reporter_ip", "code", 
        "reason", "buid", "merchant", "tid", 
        "group", "http_user_agent", "user_agent",
        "app_url", "isp", "city", "state", "country",
        "username"
    ])

logger = log.getLogger("incident", filename="incident.log")

"""
very generic 
external system can post an event
{
     "description": "Critical Test Event",
     "hostname": "r1",
     "details": "A critical event occurred on r1 running blah blah",
     "level": 7,
     "category": "prepaid.event",
     "metadata": {
        "error_stack": "....."
     }
}
"""


class Event(JSONMetaData, rm.RestModel):
    class RestMeta:
        POST_SAVE_FIELDS = ["level", "catagory"]
        SEARCH_FIELDS = ["description", "hostname"]
        VIEW_PERMS = ["view_incidents", "view_logs"]
        CREATE_PERMS = None  # allow anyone to create an event
        GRAPHS = {
            "default": {
                "graphs": {
                    "group": "basic",
                    "created_by": "basic"
                },
            },
            "detailed": {
                "graphs": {
                    "group": "basic",
                    "created_by": "basic",
                    "generic__component": "basic",
                },
            },
        }

    created = models.DateTimeField(auto_now_add=True)
    reporter_ip = models.CharField(max_length=16, blank=True, null=True, default=None, db_index=True)

    hostname = models.CharField(max_length=255, blank=True, null=True, default=None, db_index=True)
    description = models.CharField(max_length=84)
    details = models.TextField(default=None, null=True)

    level = models.IntegerField(default=0, db_index=True)
    category = models.CharField(max_length=124, db_index=True)
    # code = models.IntegerField(default=0, db_index=True)

    group = models.ForeignKey(
        "account.Group", on_delete=models.SET_NULL, 
        related_name="+", null=True, default=None)
 
    component = models.SlugField(max_length=250, null=True, blank=True, default=None)
    component_id = models.IntegerField(null=True, blank=True, default=None)

    # this allows us to bundle multiple events to an incident
    incident = models.ForeignKey(
        Incident, null=True, default=None, 
        related_name="events", on_delete=models.SET_NULL)

    def runRules(self):
        for rule in Rule.objects.filter(category=self.category).order_by("priority"):
            if rule.run(self):
                return rule
        return None

    @property
    def details_by_category(self):
        # returns detailed text based on the category settings
        # if EVENT_DETAIL_TEMPLATES is None or self.category not in EVENT_DETAIL_TEMPLATES:
        #     return self.details
        output = []
        if self.component:
            output.append(f"{self.component}({self.component_id})")
        for key in EVENT_META_KEYWORDS:
            if self.metadata.get(key, None) is not None:
                output.append(f"{key}: {self.metadata[key]}")
        if self.details:
            output.append(self.details)
            output.append("")
            output.append("")
        return "\n".join(output)

    def lookupIP(self, ip):
        GeoIP = rm.RestModel.getModel("location", "GeoIP")
        gip = GeoIP.lookup(ip)
        self.setProperty("ip", ip)
        if gip:
            self.setProperty("country", gip.country)
            self.setProperty("state", gip.state)
            self.setProperty("city", gip.city)
            self.setProperty("isp", gip.isp)

    def set_description(self, value):
        # trun desc to 84
        if value is None:
            value = ""
        if len(value) > 84:
            value = value[:80] + "..."
        self.description = value

    def on_rest_pre_save(self, request):
        if self.hostname is None:
            self.hostname = settings.HOSTNAME
        if not self.getProperty("hostname", None):
            self.setProperty("hostname", self.hostname)
        self.setProperty("category", self.category)
        if request and request.DATA.get("ip_lookup", field_type=bool):
            self.reporter_ip = request.ip
            self.lookupIP(request.ip)

    def on_rest_saved(self, request, is_new=False):
        if not is_new:
            return
        if INCIDENT_EVENT_METRICS:
            if self.hostname:
                metrics.metric(f"incident_evt_{self.hostname}", category="incident_events", min_granularity="hourly")
            metrics.metric("incident_evt", category="incident_events", min_granularity="hourly")

        self.setProperty("level", self.level)
        if request is not None:
            self.reporter_ip = request.ip
        # run through rules for the category
        hit_rule = self.runRules()
        priority = 10
        incident = None
        action_count = 0
        if hit_rule is not None:
            logger.error(f"RULE HIT: {hit_rule.name}")
            priority = hit_rule.priority
            if hit_rule.action == "ignore":
                self.save()
                return
            if hit_rule.bundle > 0:
                incident = Incident.getBundled(rule=hit_rule, event=self)

        elif self.level >= EVENT_TO_INCIDENT_LEVEL:
            # we ignore levels 4 and higher if they did not create a rule
            self.save()
            # logger.info(f"ignore event {self.pk} {self.description}")
            return

        # always create an incident 
        if incident is None:
            incident = Incident(
                rule=hit_rule, priority=priority,
                reporter_ip=self.reporter_ip,
                category=self.category,
                group=self.group,
                component=self.component, 
                component_id=self.component_id,
                hostname=self.hostname)
            if self.group is None and hit_rule is not None:
                incident.group = hit_rule.group
            if hit_rule is not None and hit_rule.action_after != 0:
                incident.state = INCIDENT_STATE_PENDING
            # TODO possibly make this smarter?
            if self.category == "ossec":
                incident.description = f"{self.hostname}: {self.description}"
            else:
                incident.description = self.description
            incident.save()
            incident.updateMeta(self)
        self.incident = incident
        self.save()
        if INCIDENT_METRICS:
            if self.hostname:
                metrics.metric(f"incidents_{self.hostname}", category="incidents", min_granularity="hourly")
            metrics.metric("incidents", category="incidents", min_granularity="hourly")

        try:
            incident.triggerAction()
        except Exception:
            logger.exception()

