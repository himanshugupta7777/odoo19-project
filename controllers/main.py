from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
import re


class StudentController(http.Controller):

    # FORM DISPLAY
    @http.route('/student-form', type='http', auth='public', website=True)
    def student_form(self, **kwargs):

        model = request.env['student.info']
        all_fields = model.sudo().fields_get()

        allowed_fields = [
            'stu_name',
            'branch',
            'roll_no',
            'description',
            'gpa',
            'gender',
            'email',
        ]

        form_fields = {k: v for k, v in all_fields.items() if k in allowed_fields}

        return request.render('new_module.student_form_page', {
            'fields': form_fields,
            'success': False,
            'field_errors': {},
        })

    # FORM SUBMIT
    @http.route('/student-form/submit',
                type='http',
                auth='public',
                website=True,
                methods=['POST'],
                csrf=True)
    def student_form_submit(self, **post):

        model = request.env['student.info']
        all_fields = model.sudo().fields_get()

        allowed_fields = [
            'stu_name',
            'branch',
            'roll_no',
            'description',
            'gpa',
            'gender',
            'email',
        ]

        form_fields = {k: v for k, v in all_fields.items() if k in allowed_fields}

        values = {}
        field_errors = {}

        # REQUIRED FIELD VALIDATION
        required_fields = ['stu_name', 'branch', 'roll_no', 'gpa', 'email']

        for field in required_fields:
            if not post.get(field):
                field_errors[field] = "This field is required."


        # EMAIL VALIDATION
        email = post.get('email')

        if email:
            email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(email_pattern, email):
                field_errors['email'] = "Invalid email format."

            existing_email = model.sudo().search([
                ('email', '=', email)
            ], limit=1)

            if existing_email:
                field_errors['email'] = "This email is already registered!"

            values['email'] = email

        # ROLL NO VALIDATION
        roll_no = post.get('roll_no')

        if roll_no:
            try:
                roll_no = int(roll_no)

                if roll_no <= 0:
                    field_errors['roll_no'] = "Roll number must be positive."

                existing_roll = model.sudo().search([
                    ('roll_no', '=', roll_no)
                ], limit=1)

                if existing_roll:
                    field_errors['roll_no'] = "This Roll Number is already assigned!"

                values['roll_no'] = roll_no

            except ValueError:
                field_errors['roll_no'] = "Roll number must be numeric."



        # OTHER FIELDS
        for field in ['stu_name', 'branch', 'description', 'gpa', 'gender']:
            if post.get(field):
                values[field] = post.get(field)

        # IF ERRORS
        if field_errors:
            return request.render('new_module.student_form_page', {
                'fields': form_fields,
                'old_values': post,
                'field_errors': field_errors,
                'success': False
            })


        # CREATE RECORD
        try:
            model.sudo().create(values)
        except ValidationError as e:
            return request.render('new_module.student_form_page', {
                'fields': form_fields,
                'old_values': post,
                'field_errors': {'general': str(e)},
                'success': False
            })

    
        # SUCCESS
        return request.render('new_module.student_form_page', {
            'fields': form_fields,
            'old_values': post,
            'field_errors': {},
            'success': True
        })
