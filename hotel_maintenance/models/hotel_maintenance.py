from odoo import api, models, fields,_
from datetime import datetime

class HotelMaintenance(models.Model):
    _name = 'hotel.maintenance'
    _description = 'Hotel Maintenance'


    #sequence
    name = fields.Char(
        required=True, readonly=True, copy=False, default=lambda self: _("New")
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("hotel.maintenance") or _("New") 

        return super().create(vals_list)
    

    room_id = fields.Many2one('hotel.room',required=True)
    employee_id = fields.Many2one("hr.employee", string='Assigned Employee' ,domain="[('job_id.name', '=', 'Maintenance')]")  
    issue_description = fields.Text(string="Solved Issue")
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ], string='Status', default='open',)


    

    requested_id = fields.Many2one("hotel.housekeeping", string="Housekeeping Request")
    maintenance_descriptionn = fields.Text(string="Maintenance Description")

    ##
    planned_start_date = fields.Datetime(copy=False)
    planned_end_date = fields.Datetime(copy=False)
    total_time = fields.Float(string='Total Time (Planned hours)', compute="_compute_total_time", store=True)

    start_time = fields.Datetime(copy=False)
    end_time = fields.Datetime(copy=False)
    actual_time = fields.Float(string='Actual Time (Spent hours)', compute='_compute_actual_time', store=True)

    def mark_in_progress(self):
        self.status = 'in_progress'
        self.start_time= datetime.now()
        self.requested_id.maintenance_status = "assigned"

    def mark_done(self):
        self.status = 'done'
        self.end_time = datetime.now()
        self.requested_id.maintenance_status = "completed"

    @api.depends('start_time', 'end_time')
    def _compute_actual_time(self):
        for record in self:
            if record.start_time and record.end_time:
                record.actual_time = (record.end_time - record.start_time).total_seconds()/3600

    @api.depends('planned_start_date', 'planned_end_date')
    def _compute_total_time(self):
        for record in self:
            if record.planned_start_date and record.planned_end_date:
                record.total_time = (record.planned_end_date - record.planned_start_date).total_seconds()/3600
    


  

