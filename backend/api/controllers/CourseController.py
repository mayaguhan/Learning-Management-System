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

@app.route("getAllCourses")
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
# def getAll():
#     """
#     Returns all courses
#     A more detailed description of the endpoint
#     ---
#     """
#     result = courseData.query.outerjoin(courseRequirement, courseData.course_id == courseRequirement.course_id, isouter=False).group_by(courseData.course_id).all()
#     # result = courseRequirement.query.all()
#     # result = courseData.query.join(courseRequirement).on()
#     print(result)
#     returnDict = {}
#     for i in range(0, len(result)):

#         # For Course object creation and Return

#         # Serialize data from database into JSON
#         courseSerialized = CourseDataSchema().dump(result[i])
#         print(courseSerialized)
        
#         returnDict[i] = courseSerialized

#     returnDict = json.dumps(returnDict)


#     return returnDict, 200