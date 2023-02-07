from uuid import uuid4

from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _

from stats.utils import store_event

from .flow import Flow
from .flow_log import FlowLog


class FlowStep(models.Model):
    ICON = "⏭️"
    flow = models.ForeignKey(
        Flow,
        on_delete=models.CASCADE,
        verbose_name=_("flow"),
        related_name="steps",
        editable=False,
    )
    site = models.ForeignKey(
        Site,
        verbose_name=_("site"),
        on_delete=models.CASCADE,
        related_name="+",
        editable=False,
    )

    order = models.PositiveSmallIntegerField(_("order"), editable=False)
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, editable=False
    )

    def get_typed_instance(self):
        return getattr(self, self.content_type.model)

    def save(self, *args, **kwargs):
        if not self.content_type_id:
            content_type = ContentType.objects.get_for_model(
                self, for_concrete_model=True
            )
            if content_type.model_class() != FlowStep:
                self.content_type = content_type
        self.site = self.flow.site
        self.id = None
        self.pk = None
        self._state.adding = True
        super().save(*args, **kwargs)

    def next_step(self):
        return FlowStep.objects.filter(flow=self.flow, order__gt=self.order).first()

    def prev_step(self):
        return FlowStep.objects.filter(flow=self.flow, order__lt=self.order).last()

    def run_next(self, flow_run):
        if next_step := self.next_step():
            next_step.run(flow_run)
        else:
            flow_run.log(FlowLog.INFO, "Last step reached")

    def run(self, flow_run):
        typed_instance = self.get_typed_instance()
        flow_run.log(FlowLog.INFO, f"Running flow step {typed_instance}")
        store_event(
            flow_run.environment,
            f"flow_step.{flow_run.flow_id}.{self.content_type.model}",
        )
        return typed_instance.step_run(flow_run)

    def wake_up(self, flow_run):
        try:
            typed_instance = self.get_typed_instance()
            flow_run.log(FlowLog.INFO, f"Waking up flow step {typed_instance}")
            return typed_instance.step_wake_up(flow_run)
        except BaseException as err:
            flow_run.log(FlowLog.ERROR, err)
            raise

    def __str__(self):
        return "%s %s" % (self.ICON, self._meta.verbose_name.title())

    class Meta:
        verbose_name = _("flow step")
        verbose_name_plural = _("flow steps")
        ordering = ("flow", "order")
        unique_together = ("flow", "order")
