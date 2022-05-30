from django.test import TestCase
from pipelines.models import PipelineRun, Pipeline
from configuration.models import Environment, Account

class PipelineRunTestCase(TestCase):

    account = None
    pipeline = None
    environment = None

    def setUp(self):
        self.account = Account.objects.create(name='testacount')
        self.environment = Environment.objects.create(account=self.account, name='testenviornment')
        self.pipeline = Pipeline.objects.create(
                account=self.account,
                name='testpipeline',
            )
        self.pipeline.environments.add(self.environment)

    def test_something(self):
        pipeline_run = PipelineRun.save_model(
            self.environment,
            self.pipeline
        )
        #self.assertEqual(lion.speak(), 'The lion says "roar"')
        