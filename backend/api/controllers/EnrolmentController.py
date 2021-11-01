from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from ..data_access.lms_user import LMSUser
from ..data_access.lms_conduct import LMSConduct

from ..data_access.lms_enrolment import LMSEnrolment
from ..data_access.lms_course import LMSCourse

db = SQLAlchemy()

# Get All Self Enrolment Request
def getallSelfEnrolmentRequest():
    enrolments = db.session.query(LMSEnrolment.learner_id, LMSUser.name, LMSUser.email,LMSUser.seniority_level, LMSUser.contact, LMSCourse.course_id, LMSCourse.course_code, LMSCourse.title, LMSCourse.outline, LMSConduct.trainer_id, LMSConduct.capacity, LMSConduct.start_date, LMSConduct.end_date, LMSConduct.start_register, LMSConduct.end_register, LMSEnrolment.status).filter(LMSUser.user_id == LMSEnrolment.learner_id, LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSConduct.course_id == LMSCourse.course_id, LMSEnrolment.status == "Request").all()


    returnArray = []

    if enrolments:
        for enrolment in enrolments:
            returnObj = {}
            returnObj["learner_id"] = enrolment[0]
            returnObj["name"] = enrolment[1]
            returnObj["email"] = enrolment[2]
            returnObj["seniority_level"] = enrolment[3]
            returnObj["contact"] = enrolment[4]
            returnObj["course_id"] = enrolment[5]
            returnObj["course_code"] = enrolment[6]
            returnObj["title"] = enrolment[7]
            returnObj["outline"] = enrolment[8]
            returnObj["trainer_id"] = enrolment[9]
            returnObj["capacity"] = enrolment[10]
            returnObj["start_date"] = enrolment[11]
            returnObj["end_date"] = enrolment[12]
            returnObj["start_register"] = enrolment[13]
            returnObj["end_register"] = enrolment[14]
            returnObj["status"] = enrolment[15]

            returnArray.append(returnObj)

        return jsonify(
            {
                "code" : 200,
                "data": returnArray
            }
        )
            


    else:
        return jsonify(
            {
                "code" : 404,
                "message":"Oops no self enrolment request exists"
            }
        ),404

# Add a new enrolment
def addANewEnrolment(data):
    enrolment = LMSEnrolment(**data)
    try:
        db.session.add(enrolment)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the enrolment."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": enrolment.to_dict()
        }
    ), 201
    