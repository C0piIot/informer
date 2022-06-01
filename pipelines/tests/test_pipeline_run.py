from django.test import TestCase
from pipelines.models import PipelineRun, Pipeline
from configuration.models import Environment, Account
from contacts.models import Contact

class PipelineRunTestCase(TestCase):

    account = None
    pipeline = None
    environment = None
    event = 'test_event'

    def setUp(self):
        self.account = Account.objects.create(name='testacount')
        self.environment = Environment.objects.create(account=self.account, name='testenviornment')
        self.contact = Contact(name='lol', key='fuu')
        self.pipeline = Pipeline.objects.create(
                account=self.account,
                name='testpipeline',
                trigger=self.event
            )
        self.pipeline.environments.add(self.environment)

    def test_something(self):
        PipelineRun.dispatch_event(self.environment, self.contact, self.event, event_payload={})

        