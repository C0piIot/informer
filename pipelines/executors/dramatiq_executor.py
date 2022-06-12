import dramatiq
from django.core import serializers


class DramatiqExecutor:

	@classmethod
	def execute_step(cls, pipeline_step, pipeline_run):
		data = serializers.serialize("json", [pipeline_step,pipeline_run])
		dramatiq_execute_step.send(data)

@dramatiq.actor
def dramatiq_execute_step(data):
	deserialized_pipeline_step, deserialized_pipeline_run = serializers.deserialize("json", data)
	deserialized_pipeline_step.object.run(deserialized_pipeline_run.object)
