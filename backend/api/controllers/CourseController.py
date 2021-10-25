# from flask.globals import request
# from api.model.user import SeniorEngineer, User
# from api.data_access.courseDataAccess import courseData, courseRequirement
# from api.schema.user import UserSchema, SeniorEngineerSchema
# from api.schema.data import CourseDataSchema 
# from sqlalchemy import func
# import json
# from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from ..data_access.app_config import app,db
from ..data_access.lms_course import Course

@app.route("/getAllCourses")
def getAllCourses():
    courses = Course.query.all()
    if courses:
        return jsonify(
            {
                "data":[course.to_dict() for course in courses]
            }
        ),200
    else:
        return jsonify(
            {
                "message":"Oops no course exists"
            }
        ),404

@app.route("/getCourseByID",method= ["POST"])
def get_course_by_ID():
    data = request.get_json()
    course_id = data["course_id"]
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        return jsonify({
            "data" : course.to_dict()
        }),200
    else:
        return jsonify({
            "message" : "No such course exists"
        }),404

@app.route("/createCourse",methods=["POST"])
def create_course():
    data = request.get_json()
    # todo:how to handle nullable course_id and course_requisite_id in object creation
    if not all(key in data.keys for key in ("course_code","title","outline","badges","active")):
        return jsonify(
            {
                "message" : "Incorrect JSON object provided"
            }
        ),500
    course_code = data["couse_code"]
    title = data["title"]
    outline = data["outline"]
    badges = data["badges"]
    active = data["active"]
    course = Course(
        course_code = course_code,
        title = title,
        outline = outline,
        badges = badges,
        active = active
    )
    if "course_requisite_id" in data.keys:
        course.course_requisite_id = data["course_requisite_id"]
    try:
        db.session.add(course)
        db.commit
    except Exception:
        return jsonify(
            {
                "message" : "Looks like there was an issue writing to the database. Try again later."
            }
        ),500

@app.route("/updateCourse",methods=["POST"])
def update_course():
    data = request.get_json()
    if not all(key in data.keys for key in ("course_id","course_requisite_id","course_code","title","outline","badge","active")):
        return jsonify({
            "message" : "Invalid input"
        }),404
    course_id = data["course_id"]
    course = Course.query.filter_by(course_id=course_id).first()
    if course:
        course_requisite_id = data["course_requisite_id"]
        course_code = data["course_code"]
        title = data["title"]
        outline = data["outline"]
        badge = data["badge"]
        active = data["active"]
        course.course_requisite_id = course_requisite_id
        course.course_code = course_code
        course.title = title
        course.outline = outline
        course.badge = badge
        course.active = active
        try:
            db.session.add(course)
            db.commit
        except Exception:
            return jsonify(
                {
                    "message" : "Looks like there was an issue writing to the database. Try again later."
                }
            ),500
    else:
        return jsonify({
            "message" : "No such course exists, update failed."
        })
