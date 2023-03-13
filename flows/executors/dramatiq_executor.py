
import dramatiq
from django.conf import settings
from django.core import serializers
from django.utils.module_loading import import_string

from accounts.models import Environment
from flows.models import FlowLog

from .base_executor import BaseExecutor


@dramatiq.actor
def dramatiq_wake_up(environment_pk, flow_run_pk_hex, flow_step_pk):
    BaseExecutor.base_wake_up(environment_pk, flow_run_pk_hex, flow_step_pk)


@dramatiq.actor
def dramatiq_run(environment_pk, flow_run_pk_hex):
    BaseExecutor.base_run(environment_pk, flow_run_pk_hex)


class DramatiqExecutor(BaseExecutor):
    @classmethod
    def run(cls, flow_run):
        dramatiq_run.send(flow_run.environment.pk, flow_run.pk.hex)

    @classmethod
    def schedule_wake_up(cls, flow_run, flow_step, time_delta):
        dramatiq_wake_up.send_with_options(
            args=(flow_run.environment.pk, flow_run.pk.hex, flow_step.pk),
            delay=time_delta.total_seconds() * 1000,
        )
