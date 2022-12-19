from odoo import fields, models, api, _


class EmployeeTransfer(models.Model):
    _name = 'employee.transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "An Employee Transfer App"

    name = fields.Char(string='Order Reference', readonly=True, default=lambda self: _('New'), check_company=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company, readonly=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)
    transfer_company_id = fields.Many2one('res.company', string='Company to Transfer',
                                          domain="[('id', '!=', company_id)]")

    request_date = fields.Datetime(string='Requested Date', default=fields.Datetime.now())
    responsible_id = fields.Many2one('res.users', string='Responsible', default=lambda self: self.env.user)
    status = fields.Selection(string='Status', copy=False,
                              selection=[('draft', 'Draft'), ('requested', 'Requested'),
                                         ('transferred', 'Transferred'), ('cancel', 'Cancelled')], default='draft',
                              tracking=True)

    @api.model
    def create(self, vals):
        # if 'company_id' in vals:
        #     self = self.with_company(vals['company_id'])
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('employee.transfer') or _('New')
        res = super(EmployeeTransfer, self).create(vals)
        return res

    def button_transfer_request(self):
        self.status = 'requested'
        print("requested")

    def button_approve(self):
        self.status = 'transferred'
        print("transferred")
        self.env['hr.employee'].create({
            'name': self.employee_id.name,
            'company_id': self.transfer_company_id.id,
            'department_id': self.employee_id.department_id.id,
        })
        print(self.employee_id)
        self.employee_id.active = False


    def button_cancel(self):
        self.status = 'cancel'
        print("cancel")

