from odoo import fields,models,api, _
import logging
_logger=logging.getLogger(__name__)
from odoo.exceptions import UserError,ValidationError

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
    grade = fields.Char(string="Grade", compute="_compute_grade", store=True)
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



    @api.constrains('roll_no')
    def _check_roll_no(self):
        for rec in self:
            if rec.roll_no < 0:
                raise ValidationError(_("Roll number cannot be negative!"))

    @api.constrains('gpa')
    def _check_gpa(self):
        for rec in self:
            if rec.gpa<=0:
                raise ValidationError(_("Gpa can't be negative!"))            

    @api.constrains('dob')
    def _check_birth_date(self):
        """ Prevent future birth dates """
        for rec in self:
            if rec.dob and rec.dob > fields.Datetime.now():
                raise ValidationError(_("The Date of Birth cannot be in the future!"))


    @api.ondelete(at_uninstall=False)
    def _prevent_delete_graduated(self):
        raise UserError("OnDelete Hit")
        _logger.info("OnDelete method called")
        """ Prevent deleting students who have already graduated """
        for rec in self:
            if rec.is_graduated:
                raise UserError(_("You cannot delete a student record once they have graduated!"))


    @api.depends('gpa')
    def _compute_grade(self):
        """ Automatically calculate Grade whenever GPA changes """
        for rec in self:
            if rec.gpa >= 3.5:
                rec.grade = 'Excellent'
            elif rec.gpa >= 2.0:
                rec.grade = 'Average'
            else:
                rec.grade = 'Below Average' 

    @api.onchange('stu_name', 'branch')
    def _onchange_student_details(self):
        """ Suggest a description live as the user types """
        if self.stu_name and self.branch:
            # This updates the screen immediately
            self.description = _("Student %s is enrolled in the %s branch.") % (self.stu_name, self.branch)
                       
            

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

        return super().write(vals)

    def unlink(self):
        if self.env.context.get('install_mode'):
            return super(MyModule, self).unlink()
        
        return super(MyModule, self).unlink()
