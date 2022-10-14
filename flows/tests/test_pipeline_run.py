from django.test import TestCase
from flows.models import FlowRun, Flow
from accounts.models import Environment, Account
from contacts.models import Contact

class FlowRunTestCase(TestCase):

    account = None
    flow = None
    environment = None
    event = 'test_event'

    def setUp(self):
        self.account = Account.objects.create(name='testacount')
        self.environment = Environment.objects.create(account=self.account, name='testenviornment')
        self.contact = Contact(name='lol', key='fuu')
        self.flow = Flow.objects.create(
                account=self.account,
                name='testflow',
                trigger=self.event
            )
        self.flow.environments.add(self.environment)

    def test_something(self):
        FlowRun.dispatch_event(self.environment, self.contact, self.event, event_payload={})

        