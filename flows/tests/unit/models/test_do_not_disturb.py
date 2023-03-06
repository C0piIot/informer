from datetime import timedelta, time, datetime, date
from unittest.mock import MagicMock, patch
from django.utils import timezone
from django.test import TestCase

from contacts.models import Contact
from flows.models import DoNotDisturb, FlowRun


class DoNotDisturbTestCase(TestCase):
    def test_step_run(self):
        flow_run = FlowRun()

        with patch('flows.models.do_not_disturb.timezone.now') as mock_now:
            now = timezone.make_aware(datetime.combine(date.today(), time(5, 0)), is_dst=False)
            mock_now.return_value = now

            doNotDisturb = DoNotDisturb(start=time(10, 0), end=time(12, 0))
            doNotDisturb.run_next = MagicMock()
            flow_run.schedule_wake_up = MagicMock()
            doNotDisturb.step_run(flow_run)
            doNotDisturb.run_next.assert_called_with(flow_run)

            doNotDisturb.start = time(3,0)
            doNotDisturb.step_run(flow_run)
            flow_run.schedule_wake_up.assert_called_with(doNotDisturb, timedelta(hours=7))

            doNotDisturb.end = time(1,0)
            doNotDisturb.step_run(flow_run)
            flow_run.schedule_wake_up.assert_called_with(doNotDisturb, timedelta(hours=20))