from odoo import models, api, _


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    @api.model
    def write(self, vals):
        res = super(HrAttendance, self).write(vals)
        if "check_out" in vals:
            for record in self:
                self._stop_running_timers(record.employee_id)
        return res

    def _stop_running_timers(self, employee):
        running_timers = self._get_running_timers(employee)
        if running_timers:
            for timer in running_timers:
                timer.button_end_work()

    def _get_running_timers(self, employee):
        """Obtain running timers for the employee."""
        employee = employee or self.env.user.employee_ids
        running = self.env["account.analytic.line"].search(
            [
                ("date_time", "!=", False),
                ("employee_id", "in", employee.ids),
                ("project_id", "!=", False),
                ("unit_amount", "=", 0),
            ]
        )
        return running
