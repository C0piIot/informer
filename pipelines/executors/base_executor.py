import uuid
from django.core import serializers
from django.conf import settings
from configuration.models import Environment
from django.utils.module_loading import import_string
from pipelines.models import PipelineLog


class BaseExecutor:

    @classmethod
    def run(cls, pipeline_run):
        pass

    @classmethod
    def schedule_wake_up(cls, pipeline_run, pipeline_step, time_delta):
        pass

    def base_wake_up(environment_pk, pipeline_run_pk_hex, pipeline_step_pk):
        storage = import_string(settings.PIPELINE_RUN_STORAGE)
        environment = Environment.objects.get(pk=environment_pk)
        pipeline_run = storage.get_pipeline_run(
            environment, 
            uuid.UUID(pipeline_run_pk_hex)
        )
        try:
            pipeline_run.pipeline_revision.steps.get(pk=pipeline_step_pk).wake_up(pipeline_run)
        except Exception as err:
            pipeline_run.log(PipelineLog.ERROR, err)
        finally:
            storage.save_pipeline_run(environment, pipeline_run)
        
    def base_run(environment_pk, pipeline_run_pk_hex):
        storage = import_string(settings.PIPELINE_RUN_STORAGE)
        environment = Environment.objects.get(pk=environment_pk)
        pipeline_run = storage.get_pipeline_run(
            environment, 
            uuid.UUID(pipeline_run_pk_hex)
        )
        try:
            if pipeline_step := pipeline_run.pipeline_revision.steps.first():
                pipeline_step.run(pipeline_run)
            else:
                pipeline_run.log(PipelineLog.WARNING, 'No steps in current pipeline')
        except Exception as err:
            pipeline_run.log(PipelineLog.ERROR, err)
        finally:
            storage.save_pipeline_run(environment, pipeline_run)
