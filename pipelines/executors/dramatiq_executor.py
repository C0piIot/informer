import dramatiq, uuid
from django.core import serializers
from django.conf import settings
from configuration.models import Environment
from django.utils.module_loading import import_string
from pipelines.models import PipelineLog
from .base_executor import BaseExecutor

class DramatiqExecutor(BaseExecutor):

    @classmethod
    def run(cls, pipeline_run):
        dramatiq_run.send(pipeline_run.environment.pk, pipeline_run.pk.hex)

    @classmethod
    def schedule_wake_up(cls, pipeline_run, pipeline_step, time_delta):
        dramatiq_wake_up.send_with_options(args=(pipeline_run.environment.pk, pipeline_run.pk.hex, pipeline_step.pk), delay=time_delta.total_seconds() * 1000)


@dramatiq.actor
def dramatiq_wake_up(environment_pk, pipeline_run_pk_hex, pipeline_step_pk):
    BaseExecutor.base_wake_up(environment_pk, pipeline_run_pk_hex, pipeline_step_pk)
        

@dramatiq.actor
def dramatiq_run(environment_pk, pipeline_run_pk_hex):
    BaseExecutor.base_run(environment_pk, pipeline_run_pk_hex)
    