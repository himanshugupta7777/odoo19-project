from odoo import fields,models

class MyModule(models.Model):
    _name = 'my_module.my_module'
    _description = 'Description'
    _rec_name='stu_name'
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


    
