from datetime import date, datetime, time, timedelta
from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from contacts.models import Contact
from flows.models import DoNotDisturb, FlowRun


class DoNotDisturbTestCase(TestCase):
    def test_step_run(self):
        flow_run = FlowRun()

        with patch('flows.models.do_not_disturb.timezone.now') as mock_now:
            now = timezone.make_aware(datetime.combine(date.today(), time(5, 0)), is_dst=False)
            mock_now.return_value = now

            doNotDisturb = DoNotDisturb(start=time(10, 0), end=time(12, 0))
            self.assertEqual(str(doNotDisturb), f"{DoNotDisturb.ICON} Do Not Disturb {doNotDisturb.start}-{doNotDisturb.end}")

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

            doNotDisturb.step_wake_up(flow_run)
            doNotDisturb.run_next.assert_called_with(flow_run)

    def test_name(self):

        doNotDisturb = DoNotDisturb(start=time(10, 0), end=time(12, 0))
        self.assertEqual(str(doNotDisturb), f"{DoNotDisturb.ICON} Do Not Disturb {doNotDisturb.start}-{doNotDisturb.end}")



    def test_clean(self):

        doNotDisturb = DoNotDisturb(start=time(10, 0), end=time(10, 0))
        with self.assertRaises(ValidationError):
            doNotDisturb.clean()


