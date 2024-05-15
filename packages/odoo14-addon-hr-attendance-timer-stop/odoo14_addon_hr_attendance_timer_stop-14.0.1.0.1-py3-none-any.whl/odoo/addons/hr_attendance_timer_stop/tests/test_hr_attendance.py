# tests/test_hr_attendance.py
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class TestHrAttendance(TransactionCase):

    def setUp(self):
        super(TestHrAttendance, self).setUp()
        self.employee = self.env["hr.employee"].create({"name": "Test Employee"})
        self.project = self.env["project.project"].create({"name": "Test Project"})
        self.timesheet_line = self.env["account.analytic.line"].create(
            {
                "name": "Test Timesheet Line",
                "employee_id": self.employee.id,
                "project_id": self.project.id,
                "date_time": datetime.now() - timedelta(hours=1),
                "unit_amount": 0,
            }
        )
        self.attendance = self.env["hr.attendance"].create(
            {
                "employee_id": self.employee.id,
                "check_in": datetime.now() - timedelta(hours=8),
            }
        )

    def test_stop_running_timer_on_checkout(self):
        self.assertEqual(
            self.timesheet_line.unit_amount,
            0,
            "The timesheet should have zero duration initially",
        )

        # Perform the checkout action
        self.attendance.write({"check_out": datetime.now()})

        # Reload the timesheet line to get updated values
        self.timesheet_line.invalidate_cache()

        self.assertNotEqual(
            self.timesheet_line.unit_amount,
            0,
            "The timesheet should not have zero duration after checkout",
        )
        self.assertAlmostEqual(
            self.timesheet_line.unit_amount,
            1,
            delta=0.1,
            msg="The timesheet duration should be approximately 1 hour",
        )

    def test_no_running_timers(self):
        # Ensure no timers are running initially
        self.timesheet_line.write({"unit_amount": 1})

        # Perform the checkout action
        self.attendance.write({"check_out": datetime.now()})

        # Ensure no errors are raised and no timers are stopped
        self.timesheet_line.invalidate_cache()
        self.assertEqual(
            self.timesheet_line.unit_amount,
            1,
            "The timesheet duration should remain unchanged",
        )

    def test_multiple_running_timers(self):
        # Create another running timer
        self.timesheet_line_2 = self.env["account.analytic.line"].create(
            {
                "name": "Another Test Timesheet Line",
                "employee_id": self.employee.id,
                "project_id": self.project.id,
                "date_time": datetime.now() - timedelta(hours=2),
                "unit_amount": 0,
            }
        )

        with self.assertRaises(
            UserError, msg="Multiple running timers should raise a UserError"
        ):
            self.attendance.write({"check_out": datetime.now()})
