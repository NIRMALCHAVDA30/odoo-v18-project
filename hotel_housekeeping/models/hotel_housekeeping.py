from odoo import api, models, fields,_
from datetime import datetime

class HotelHousekeeping(models.Model):
    _name = "hotel.housekeeping"
    _description = "Hotel Housekeeping"

    #sequence
    name = fields.Char(
        required=True, readonly=True, copy=False, default=lambda self: _("New")
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("hotel.housekeeping") or _("New") 

        return super().create(vals_list)
    

    room_id = fields.Many2one("hotel.room", required=True)
    employee_id = fields.Many2one("hr.employee")
    # floor = fields.Integer(required=True)
    service = fields.Selection([
        ("floor_cleaning", "Floor Cleaning"),
        ("room_cleaning", "Room Cleaning"),
        ("laundry", "Laundry"),
        ("other", "Other")
    ], copy=False)

    planned_start_date = fields.Datetime(copy=False)
    planned_end_date = fields.Datetime(copy=False)
    total_time = fields.Float(string='Total Time (Planned hours)', compute="_compute_total_time", store=True)


    cleaning_status = fields.Selection([
        ("pending" , "Pending"),
        ("in_maintenance", "In Progress"),
        ("cleaned", "Cleaned"),
        ("discard" , "Discard"),
    ] ,default="pending")

    start_time = fields.Datetime(copy=False)
    end_time = fields.Datetime(copy=False)
    actual_time = fields.Float(string='Actual Time (Spent hours)', compute='_compute_actual_time', store=True)

    def action_take(self):
            self.cleaning_status = 'in_maintenance'
            self.start_time= datetime.now()
            self.room_id.housekeeping_status = 'in_maintenance'
            self.request_id.status = 'assigned'
        

    def action_done(self):
            self.cleaning_status = 'cleaned'
            self.end_time = datetime.now()
            self.room_id.housekeeping_status = 'cleaned'
            self.request_id.status = 'completed'

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

    def action_discard(self):
         self.cleaning_status = "discard"


    
    request_id = fields.Many2one("housekeeping.request", string="Housekeeping Request", ondelete="cascade")
    description = fields.Text(string="Requested Description")


    ###maintenance
    maintenance_status = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent to Maintenance'),
        ('assigned', 'Assigned to Staff'),
        ('completed', 'Completed')
    ], default='draft')

    maintenance_descriptionn = fields.Text()

    def action_send_to_maintenance(self):
        maintenance_request = self.env['hotel.maintenance'].create({
            'requested_id': self.id,
            'room_id': self.room_id.id,
            'maintenance_descriptionn': self.maintenance_descriptionn,
        })

        self.maintenance_status = "sent"

        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'hotel.maintenance',
        #     'view_mode': 'list,form',
        #     'res_id': maintenance_request.id,
        #     'target': 'current',
        # }

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Request Sent',
                'type': 'success',
                'message': " request sent to maintenance successfully ",
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
    
        


    
    