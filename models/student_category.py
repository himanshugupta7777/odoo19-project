from odoo import models, fields

class StudentCategory(models.Model):
    _name = 'student.category'
    _description = 'Student Category'

    name = fields.Char(required=True)
