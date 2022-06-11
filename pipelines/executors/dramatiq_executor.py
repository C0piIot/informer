import dramatiq

class DramatiqExecutor:

	@classmethod
	def execute_step(cls, pipeline_step, pipeline_run):
		dramatiq_execute_step.send(pipeline_step, pipeline_run)



@dramatiq.actor
def dramatiq_execute_step(pipeline_step, pipeline_run):
	pipeline_step.run()