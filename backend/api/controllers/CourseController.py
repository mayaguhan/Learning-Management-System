from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from ..data_access.classes import LMSCourse

db = SQLAlchemy()

# Get all courses
def getAllCourses():
    courses = LMSCourse.query.all()
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
