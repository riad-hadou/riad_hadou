
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse, abort
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
api = Api(app)
auth = HTTPTokenAuth(scheme='Bearer')


students = {}


tokens = {
    "secrettoken123": "user1",
    "anothersecrettoken456": "user2"
}


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


student_put_args = reqparse.RequestParser()
student_put_args.add_argument("name", type=str, help="Name of the student is required", required=True)
student_put_args.add_argument("age", type=int, help="Age of the student", required=True)
student_put_args.add_argument("grade", type=float, help="Grade of the student", required=True)


def abort_if_student_id_doesnt_exist(student_id):
    if student_id not in students:
        abort(404, message="Could not find student.")


def abort_if_student_exists(student_id):
    if student_id in students:
        abort(409, message="Student already exists with that ID")


class Student(Resource):
    @auth.login_required
    def get(self, student_id):
        abort_if_student_id_doesnt_exist(student_id)
        return students[student_id]

    @auth.login_required
    def put(self, student_id):
        args = student_put_args.parse_args()
        students[student_id] = args
        return students[student_id], 201

    @auth.login_required
    def delete(self, student_id):
        abort_if_student_id_doesnt_exist(student_id)
        del students[student_id]
        return '', 204


api.add_resource(Student, "/student/<int:student_id>")


if __name__ == "__main__":
    app.run(debug=True)
