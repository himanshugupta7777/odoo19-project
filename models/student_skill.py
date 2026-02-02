from odoo import models,fields

class StudentSkill(models.Model):
    _name='student.skill'
    _description='Student Skill'

    name=fields.Char(string="Skill Name",required=True)