class BasicExecutor:

	@classmethod
	def execute_step(cls, pipeline_step, pipeline_run):
		pipeline_step.run(pipeline_run)