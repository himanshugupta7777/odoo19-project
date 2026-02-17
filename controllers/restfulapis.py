from odoo import http
from odoo.http import request
import json

class StudentAPI(http.Controller):
    #reading record of all students

    @http.route('/api/students', type='http', auth='public', methods=['GET'], csrf=False)
    # url,type,method,auth
    def get_students(self):
        students = request.env['student.info'].sudo().search([])

        data = []
        for s in students:
            data.append({
                "id": s.id,
                "name": s.stu_name,
                "email": s.email,
                "gpa": s.gpa
            })

        return request.make_json_response(data)


    #create

    @http.route('/api/student/create', type='http', auth='public', methods=['POST'], csrf=False)
    def create_student(self, **kwargs):
        # **kwargs is used for converting all arguments in dictionary format
        try:

            data = json.loads(request.httprequest.data)

            student = request.env['student.info'].sudo().create(data)

            return request.make_json_response({
                "status": "success",
                "id": student.id,
                "name": student.display_name
            }, status=201)

        except Exception as e:
            return request.make_json_response({
                "status": "error",
                "message": str(e)
            }, status=422)



    # UPDATE
    @http.route('/api/student/<int:student_id>', type='http', auth='public', methods=['PUT'], csrf=False)
    def update_student(self, student_id, **kwargs):
        try:
            data = json.loads(request.httprequest.data)

            student = request.env['student.info'].sudo().browse(student_id)

            if not student.exists():
                return request.make_json_response({
                    "status": "error",
                    "message": "Student not found"
                }, status=404)

            student.write(data)

            return request.make_json_response({
                "status": "success",
                "message": "Student updated successfully"
            }, status=200)

        except Exception as e:
            return request.make_json_response({
                "status": "error",
                "message": str(e)
            }, status=422)



     # DELETE
    @http.route('/api/student/<int:student_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_student(self, student_id, **kwargs):
        try:
            student = request.env['student.info'].sudo().browse(student_id)

            if not student.exists():
                return request.make_json_response({
                    "status": "error",
                    "message": "Student not found"
                }, status=404)

            student.unlink()

            return request.make_json_response({
                "status": "success",
                "message": "Student deleted successfully"
            }, status=200)

        except Exception as e:
            return request.make_json_response({
                "status": "error",
                "message": str(e)
            }, status=422)
        
