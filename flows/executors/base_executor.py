import uuid

from django.conf import settings
from django.utils.module_loading import import_string

from accounts.models import Environment
from flows.models import FlowLog
from stats.utils import store_events


class BaseExecutor:
    @classmethod
    def run(cls, flow_run):
        pass

    @classmethod
    def schedule_wake_up(cls, flow_run, flow_step, time_delta):
        pass

    def base_wake_up(environment_pk, flow_run_pk_hex, flow_step_pk):
        storage = import_string(settings.FLOW_RUN_STORAGE)
        environment = Environment.objects.get(pk=environment_pk)
        flow_run = storage.get_flow_run(
            environment, uuid.UUID(flow_run_pk_hex))
        try:
            flow_run.flow_revision.steps.get(pk=flow_step_pk).wake_up(flow_run)
        except Exception as err:
            flow_run.log(FlowLog.ERROR, err)
        finally:
            storage.save_flow_run(environment, flow_run)

    def base_run(environment_pk, flow_run_pk_hex):
        storage = import_string(settings.FLOW_RUN_STORAGE)
        environment = Environment.objects.get(pk=environment_pk)
        flow_run = storage.get_flow_run(
            environment, uuid.UUID(flow_run_pk_hex))
        store_events(flow_run.environment, [f"flow_start.{flow_run.flow_id}"])
        try:
            if flow_step := flow_run.flow_revision.steps.first():
                flow_step.run(flow_run)
            else:
                flow_run.log(FlowLog.WARNING, "No steps in current flow")
        except Exception as err:
            flow_run.log(FlowLog.ERROR, err)
        finally:
            storage.save_flow_run(environment, flow_run)
