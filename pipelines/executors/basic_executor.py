class BasicExecutor:

	@classmethod
	def execute_step(cls, pipeline_run, pipeline_step):
		pipeline_step.run(pipeline_run)