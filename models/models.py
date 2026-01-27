from odoo import fields,models,api, _

class MyModule(models.Model):
    _name = 'my_module.my_module'
    _description = 'Description'
    _rec_name='reference_no'
    reference_no = fields.Char(string="Student ID", required=True, copy=False, 
    readonly=True, default=lambda self: _('New'))
    stu_name = fields.Char(string="Name")
    branch = fields.Char(string="Branch")
    roll_no = fields.Integer(string="Roll No")
    description=fields.Text(string="Description")
    dob = fields.Datetime(string="Date and time of birth", required=True)
    is_graduated = fields.Boolean(string="Graduated?")
    gpa = fields.Float( digits=(12, 2))
    student_image=fields.Binary(string="Student Photo")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", default='male')
    
    previous_school=fields.Char(string="Previous School Details")
    admission_date=fields.Date(string="admission date")
    scholarship_details=fields.Char(string="scholarship details")




    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference_no', _('New')) == _('New'):
                vals['reference_no'] = self.env['ir.sequence'].next_by_code('student.details') or _('New')
        return super(MyModule, self).create(vals_list)



    
