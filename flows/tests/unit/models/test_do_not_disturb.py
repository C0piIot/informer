""" Do not disturb unit tests """
from datetime import date, datetime, time, timedelta
from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from flows.models import DoNotDisturb, FlowRun


class DoNotDisturbTestCase(TestCase):
    """ Do not disturb step test case """

    def test_step_run(self):
        flow_run = FlowRun()

        with patch("flows.models.do_not_disturb.timezone.now") as mock_now:
            now = timezone.make_aware(
                datetime.combine(date.today(), time(5, 0))
            )
            mock_now.return_value = now

            do_not_disturb = DoNotDisturb(start=time(10, 0), end=time(12, 0))
            self.assertEqual(
                str(do_not_disturb),
                f"{DoNotDisturb.ICON} Do Not Disturb "
                f"{do_not_disturb.start}-{do_not_disturb.end}",
            )

            do_not_disturb.run_next = MagicMock()
            flow_run.schedule_wake_up = MagicMock()
            do_not_disturb.step_run(flow_run)
            do_not_disturb.run_next.assert_called_with(flow_run)

            do_not_disturb.start = time(3, 0)
            do_not_disturb.step_run(flow_run)
            flow_run.schedule_wake_up.assert_called_with(
                do_not_disturb, timedelta(hours=7)
            )

            do_not_disturb.end = time(1, 0)
            do_not_disturb.step_run(flow_run)
            flow_run.schedule_wake_up.assert_called_with(
                do_not_disturb, timedelta(hours=20)
            )

            do_not_disturb.step_wake_up(flow_run)
            do_not_disturb.run_next.assert_called_with(flow_run)

    def test_name(self):
        do_not_disturb = DoNotDisturb(start=time(10, 0), end=time(12, 0))
        self.assertEqual(
            str(do_not_disturb),
            f"{do_not_disturb.ICON} Do Not Disturb "
            f"{do_not_disturb.start}-{do_not_disturb.end}"
        )

    def test_clean(self):
        do_not_disturb = DoNotDisturb(start=time(10, 0), end=time(10, 0))
        with self.assertRaises(ValidationError):
            do_not_disturb.clean()
