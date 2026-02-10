from odoo import models, fields, api

class UpdateBranchWizard(models.TransientModel):
    _name = 'update.branch.wizard'
    _description = 'Wizard to Update Student Branch'

    new_branch = fields.Char(string="New Branch", required=True)
    # Use default=lambda to automatically pick the student you are currently viewing
    student_ids = fields.Many2many(
        'student.info', 
        string="Students",
        default=lambda self: self.env.context.get('active_ids')
    )

    def action_apply(self):
        # This updates the branch for all students selected in the wizard
        self.student_ids.write({'branch': self.new_branch})
        return {'type': 'ir.actions.act_window_close'}
