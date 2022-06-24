import dramatiq, uuid
from django.core import serializers
from django.conf import settings
from configuration.models import Environment
from django.utils.module_loading import import_string


class DramatiqExecutor:

    @classmethod
    def run(cls, pipeline_run):
        dramatiq_run.send(pipeline_run.environment.pk, pipeline_run.pk.hex)

    @classmethod
    def schedule_wake_up(cls, pipeline_run, pipeline_step, time_delta):
        dramatiq_wake_up.send_with_options(args=(pipeline_run.environment.pk, pipeline_run.pk.hex, pipeline_step.pk), delay=time_delta.total_seconds() * 1000)


@dramatiq.actor
def dramatiq_wake_up(environment_pk, pipeline_run_pk_hex, pipeline_step_pk):
    pipeline_run = import_string(settings.PIPELINE_RUN_STORAGE).get_pipeline_run(
        Environment.objects.get(pk=environment_pk), 
        uuid.UUID(pipeline_run_pk_hex)
    )

    pipeline_run.pipeline_revision.steps.get(pk=pipeline_step_pk).wake_up(pipeline_run)
        

@dramatiq.actor
def dramatiq_run(environment_pk, pipeline_run_pk_hex):
    pipeline_run = import_string(settings.PIPELINE_RUN_STORAGE).get_pipeline_run(
        Environment.objects.get(pk=environment_pk), 
        uuid.UUID(pipeline_run_pk_hex)
    )

    if pipeline_step := pipeline_run.pipeline_revision.steps.first():
        pipeline_step.run(pipeline_run)
    else:
        pipeline_run.log(PipelineLog.WARNING, 'No steps in current pipeline')