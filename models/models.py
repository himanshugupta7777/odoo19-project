from odoo import fields,models,api, _
import logging
_logger=logging.getLogger(__name__)
from odoo.exceptions import UserError

class MyModule(models.Model):
    _name = 'student.info'
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
    user_id = fields.Many2one(
    'res.users',
    default=lambda self: self.env.user)  #for record rules

    category_id = fields.Many2one(
    'student.category',   #targeted model name
    string="Categories",

)    #for student_category model

    subject_ids=fields.One2many(
        'student.subject',
        'student_id',
        string="Subjects"
    )

    skills_ids=fields.Many2many(
        'student.skill',
        string="Skills"
    )
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference_no', _('New')) == _('New'):
                vals['reference_no'] = self.env['ir.sequence'].next_by_code('student.details') or _('New')
        return super(MyModule, self).create(vals_list)


    def copy(self, default=None):
        default = dict(default or {})
        default['gpa'] = 0.0
        default['roll_no']= 0
        return super().copy(default)

    def read(self,fields=None,load='_classic_read'):
        _logger.info("Read method called")
        return super().read(fields,load)


    def write(self, vals):
        if self.env.context.get('install_mode'):
            return super().write(vals)

        for rec in self:
            if rec.is_graduated and 'gpa' in vals:
                raise UserError("Graduated student GPA can't be updated")
            if 'roll_no' in vals and vals.get('roll_no', 0) < 0:
                raise UserError("Roll number can't be negative")

        return super().write(vals)

    def unlink(self):
        if self.env.context.get('install_mode'):
            return super(MyModule, self).unlink()

        for rec in self:
            if rec.is_graduated:
                raise UserError("Graduated student can't be deleted")
        return super(MyModule, self).unlink()
