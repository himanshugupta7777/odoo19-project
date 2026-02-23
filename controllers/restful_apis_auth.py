from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class StudentAPI(http.Controller):

    # GET ALL STUDENTS
    @http.route('/api/students',
                type='http',
                auth='user',
                methods=['GET'],
                csrf=False)
    def get_students(self):

        _logger.info("GET /api/students called by %s", request.env.user.name)
        print("USER:", request.env.user.name)
        print("IS SUPERUSER:", request.env.user.id == 1)

        students = request.env['student.info'].search([])

        data = [{
            "id": s.id,
            "name": s.stu_name,
            "email": s.email,
            "gpa": s.gpa
        } for s in students]

        return request.make_json_response(data)


    # CREATE STUDENT
    @http.route('/api/students',
                type='http',
                auth='user',
                methods=['POST'],
                csrf=False)
    def create_student(self, **kwargs):

        try:
            data = json.loads(request.httprequest.data or "{}")

            student = request.env['student.info'].create(data)

            return request.make_json_response({
                "status": "success",
                "id": student.id,
                "name": student.display_name
            }, status=201)

        except Exception:
            _logger.exception("Create Student API Error")
            return request.make_json_response({
                "status": "error",
                "message": "Internal Server Error"
            }, status=500)


    # UPDATE STUDENT
    @http.route('/api/students/<int:student_id>',
                type='http',
                auth='user',
                methods=['PUT'],
                csrf=False)
    def update_student(self, student_id, **kwargs):

        try:
            data = json.loads(request.httprequest.data or "{}")

            student = request.env['student.info'].browse(student_id)

            if not student.exists():
                return request.make_json_response({
                    "status": "error",
                    "message": "Student not found"
                }, status=404)

            student.write(data)

            return request.make_json_response({
                "status": "success",
                "message": "Student updated successfully"
            })

        except Exception:
            _logger.exception("Update Student API Error")
            return request.make_json_response({
                "status": "error",
                "message": "Internal Server Error"
            }, status=500)


    # DELETE STUDENT
    @http.route('/api/students/<int:student_id>',
                type='http',
                auth='user',
                methods=['DELETE'],
                csrf=False)
    def delete_student(self, student_id, **kwargs):

        try:
            student = request.env['student.info'].browse(student_id)

            if not student.exists():
                return request.make_json_response({
                    "status": "error",
                    "message": "Student not found"
                }, status=404)

            student.unlink()

            return request.make_json_response({
                "status": "success",
                "message": "Student deleted successfully"
            })

        except Exception:
            _logger.exception("Delete Student API Error")
            return request.make_json_response({
                "status": "error",
                "message": "Internal Server Error"
            }, status=500)
