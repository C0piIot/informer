import ssl
from urllib import request
from urllib.parse import urlparse

from django.db import models
from django.template import Context, Template
from django.utils.translation import gettext_lazy as _

from .flow_log import FlowLog
from .flow_step import FlowStep


class Webhook(FlowStep):

    class Meta:
        verbose_name = _("webhook")
        verbose_name_plural = _("webhooks")
    ICON = "🌐"
    CONTENT_TYPES = (
        "application/x-www-form-urlencoded",
        "application/json",
        "application/xml",
        "text/plain",
        "text/html",
    )
    METHODS = (
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    )
    url = models.CharField(_("url"), max_length=500)
    method = models.CharField(
        _("method"), max_length=6, choices=((m, m) for m in METHODS)
    )
    contenttype = models.CharField(
        _("Content type"), max_length=50, choices=((e, e) for e in CONTENT_TYPES)
    )
    body = models.TextField(_("body"), blank=True)
    skip_ssl = models.BooleanField(
        _("Skip https certificate validation"),
        default=False,
        help_text=_("Allows to connect to insecure webhooks"),
    )

    def step_run(self, flow_run):
        context = Context(flow_run.event_payload, autoescape=False)
        context.update(
            {
                "contact": flow_run.contact,
            }
        )

        body = Template(self.body).render(context)
        url = Template(self.url).render(context)

        request_context = None
        if self.skip_ssl:
            request_context = ssl.create_default_context()
            request_context.check_hostname = False
            request_context.verify_mode = ssl.CERT_NONE

        req = request.Request(
            url,
            headers={"Content-Type": self.contenttype},
            method=self.method,
            data=body.encode("utf-8"),
        )

        with request.urlopen(req, timeout=3, context=request_context) as response:
            flow_run.log(
                FlowLog.INFO,
                "Webhook %s %s response: %s" % (self.method, url, response.getcode()),
            )

        self.run_next(flow_run)

    def __str__(self):
        return f"{super().__str__()} {self.method} {urlparse(self.url).netloc}"
