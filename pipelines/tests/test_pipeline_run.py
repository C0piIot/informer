from django.test import TestCase
from pipelines.models import PipelineRun
from configuration.models import Environment, Account

class PipelineRunTestCase(TestCase):

    pipeline = None

    def setUp(self):
        account = Account.objects.create(name='testacount')
        environments = Environment.objects.create(account=account, name='testenviornment')
        self.pipeline = PipelineRun(
                event='testevent',
                user_key='testuserkey',
            )
        PipelineRun.save_model(
            environment,
            self.pipeline
        )

    def test_something(self):
        
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')