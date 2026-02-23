from odoo import fields,models,api, _
import logging
_logger=logging.getLogger(__name__)
from odoo.exceptions import UserError,ValidationError
from datetime import date,timedelta
import time


class StudentBase(models.AbstractModel):
    _name = 'student.base'
    _description = 'Shared Person Logic'

    dob = fields.Datetime(string="Date and time of birth")
    birthday_this_year = fields.Date(
        string="Birthday(This Year)",
        compute="_compute_birthday_this_year",
        store=True
    )

    @api.constrains('dob')
    def _check_birth_date(self):
        for rec in self:
            if rec.dob and rec.dob > fields.Datetime.now():
                raise ValidationError(_("The Date of Birth cannot be in the future!"))

    @api.depends('dob')
    def _compute_birthday_this_year(self):
        today = date.today()
        for rec in self:
            if rec.dob:
                rec.birthday_this_year = rec.dob.date().replace(year=today.year)
            else:
                rec.birthday_this_year = False



class MyModule(models.Model):
    _name = 'student.info'
    _description = 'Student Info'
    _inherit = ['mail.thread', 'mail.activity.mixin','student.base']
    _rec_name='reference_no'
    reference_no = fields.Char(string="Student ID", required=True, copy=False, 
    readonly=True, default=lambda self: _('New'))
    stu_name = fields.Char(string="Name")
    branch = fields.Char(string="Branch")
    roll_no = fields.Integer(string="Roll No")
    description=fields.Text(string="Description")
    # dob = fields.Datetime(string="Date and time of birth", required=True)
    is_graduated = fields.Boolean(string="Graduated?")
    gpa = fields.Float( digits=(12, 2))
    _order='reference_no desc'
    student_image=fields.Binary(string="Student Photo")
    grade = fields.Char(string="Grade",store=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender", default='male')
    
    previous_school=fields.Char(string="Previous School Details")
    active = fields.Boolean(default=True) 
    admission_date=fields.Date(string="admission date")
    scholarship_details=fields.Char(string="scholarship details")
    # birthday_this_year=fields.Date(
    #     string="Birthday(This Year)",
    #     compute="_compute_birthday_this_year",
    #     store=True
    # )
    email=fields.Char(string="Student Email")
    # _unique_email=models.Constraint(
    #     'UNIQUE(email)',
    #     'This email is already registered!'
    # )

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
    message_ids = fields.One2many(
    'mail.message',
    'res_id',
    domain=lambda self: [('model', '=', self._name)],
    string='Messages',
    readonly=True
    )







    def action_promote_student(self):
        for rec in self:
            if rec.gpa and rec.gpa >= 7.5:
                rec.write({
                    'grade': 'Top Performer'
                })
                rec.message_post(
                    body="Student promoted to Top Performer based on GPA."
                )
            else:
                raise UserError("Student GPA must be 7.5 or higher to promote.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference_no', _('New')) == _('New'):
                vals['reference_no'] = self.env['ir.sequence'].next_by_code('student.details') or _('New')
        return super(MyModule, self).create(vals_list)


    @api.constrains('email')
    def _check_unique_email(self):
        for rec in self:
            if rec.email:
                existing = self.search([
                    ('email', '=', rec.email),
                    ('id', '!=', rec.id)
                ], limit=1)
                if existing:
                    raise ValidationError("This email is already registered!")


    @api.constrains('roll_no')
    def _check_unique_roll_no(self):
        for rec in self:
            if rec.roll_no:
                existing = self.search([
                    ('roll_no', '=', rec.roll_no),
                    ('id', '!=', rec.id)
                ], limit=1)
                if existing:
                    raise ValidationError("This Roll Number is already assigned!")
                


    @api.constrains('roll_no')
    def _check_roll_no(self):
        for rec in self:
            if rec.roll_no < 0:
                raise ValidationError(_("Roll number cannot be negative!"))

    @api.constrains('gpa')
    def _check_gpa(self):
        for rec in self:
            if rec.gpa and rec.gpa <= 0:
                raise ValidationError(_("Gpa can't be negative or zero!"))
           

    # @api.constrains('dob')
    # def _check_birth_date(self):
    #     """ Prevent future birth dates """
    #     for rec in self:
    #         if rec.dob and rec.dob > fields.Datetime.now():
    #             raise ValidationError(_("The Date of Birth cannot be in the future!"))

    # @api.depends('dob')
    # def _compute_birthday_this_year(self):
    #     today=date.today()
    #     for rec in self:
    #         if rec.dob:
    #             rec.birthday_this_year=rec.dob.date().replace(year=today.year)
    #         else:
    #             rec.birthday_this_year=False   



    def _cron_send_birthday_emails(self):
           today=date.today()

           students=self.search([
            ('birthday_this_year','>=',today),
            ('birthday_this_year','<',today+timedelta(days=1)),
            ('email','!=',False),
           ])

           template=self.env.ref(
            'new_module.email_template_student_birthday',
            raise_if_not_found=False
           )
           for student in students:
                if template:
                    template.send_mail(student.id,force_send=True)
                            #cron job method    




    
    def cron_first_task(self):
        _logger.info("ODOO19 CRON FIRST STARTED (priority=1)")
        time.sleep(5)
        _logger.info("ODOO19 CRON FIRST FINISHED")

    def cron_second_task(self):
        _logger.info("ODOO19 CRON SECOND STARTED (priority=1)")
        time.sleep(5)
        _logger.info("ODOO19 CRON SECOND FINISHED")
         


    @api.ondelete(at_uninstall=False)
    def _prevent_delete_graduated(self):
        _logger.info("OnDelete method called")
        """ Prevent deleting students who have already graduated """
        for rec in self:
            if rec.is_graduated:
                raise UserError(_("You cannot delete a student record once they have graduated!"))


    @api.onchange('gpa')
    def _on_change(self):
        """ Automatically calculate Grade whenever GPA changes """
        _logger.info("Computing Grade for GPA: %s", self.gpa) 
        for rec in self:
            if rec.gpa >= 3.5:
                rec.grade = 'Excellent'
            elif rec.gpa >= 2.0:
                rec.grade = 'Average'
            else:
                rec.grade = 'Below Average' 
        _logger.info("Grade set to: %s", rec.grade)              

    @api.onchange('stu_name', 'branch')
    def _onchange_student_details(self):
        # import pdb;pdb.set_trace()
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




# inherting sale order        
class SaleOrder(models.Model):
    _inherit = 'sale.order'  # Use a string, not a list

    student_id = fields.Many2one(
        'student.info', 
        string="Related Student",
    )
    student_display_name = fields.Char(
        string="Student Name",
        related="student_id.stu_name", 
        readonly=True
    )


class Website(models.Model):
    _inherit='website'

    student_id = fields.Many2one(
        'student.info', 
        string="Related Student",
    )
    student_display_name = fields.Char(
        string="Student Name",
        related="student_id.stu_name", 
        readonly=True
    )


    