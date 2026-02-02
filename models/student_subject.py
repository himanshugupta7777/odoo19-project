from odoo import models, fields

class StudentSubject(models.Model):
    _name = 'student.subject'
    _description = 'Student Subjects'

    name = fields.Char(string="Subject Name", required=True)
    marks = fields.Float(string="Marks")

    student_id = fields.Many2one(
        'student.info',     # parent model
        string="Student"
    )
