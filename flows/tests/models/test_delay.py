from django.test import TestCase
from flows.models import Delay, FlowRun, FlowLog
from datetime import timedelta
from contacts.models import Contact
from unittest.mock import MagicMock


class DelayTestCase(TestCase):
    def test_step_run(self):
        flow_run = FlowRun()
        time = timedelta(hours=1)
        delay = Delay(time=time)

        flow_run.schedule_wake_up = MagicMock()
        delay.step_run(flow_run)
        flow_run.schedule_wake_up.assert_called_with(delay, time)

        delay.run_next = MagicMock()
        delay.step_wake_up(flow_run)
        delay.run_next.assert_called_with(flow_run)
