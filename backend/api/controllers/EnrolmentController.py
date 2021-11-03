from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

from ..data_access.lms_user import LMSUser
from ..data_access.lms_conduct import LMSConduct

from ..data_access.lms_enrolment import LMSEnrolment
from ..data_access.lms_course import LMSCourse

db = SQLAlchemy()

# Get All Self Enrolment Request (HR)
def getallSelfEnrolmentRequest():
    enrolments = db.session.query(LMSEnrolment.learner_id, LMSEnrolment.conduct_id, LMSUser.name, LMSUser.email,LMSUser.seniority_level, LMSUser.contact, LMSCourse.course_id, LMSCourse.course_code, LMSCourse.title, LMSCourse.outline, LMSConduct.trainer_id, LMSConduct.capacity, LMSConduct.start_date, LMSConduct.end_date, LMSConduct.start_register, LMSConduct.end_register, LMSEnrolment.status).filter(LMSUser.user_id == LMSEnrolment.learner_id, LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSConduct.course_id == LMSCourse.course_id, LMSEnrolment.status == "Request").all()

    returnArray = []
    if enrolments:
        for enrolment in enrolments:
            returnObj = {}
            returnObj["learner_id"] = enrolment[0]
            returnObj["conduct_id"] = enrolment[1]
            returnObj["name"] = enrolment[2]
            returnObj["email"] = enrolment[3]
            returnObj["seniority_level"] = enrolment[4]
            returnObj["contact"] = enrolment[5]
            returnObj["course_id"] = enrolment[6]
            returnObj["course_code"] = enrolment[7]
            returnObj["title"] = enrolment[8]
            returnObj["outline"] = enrolment[9]
            returnObj["trainer_id"] = enrolment[10]
            returnObj["capacity"] = enrolment[11]
            returnObj["start_date"] = enrolment[12]
            returnObj["end_date"] = enrolment[13]
            returnObj["start_register"] = enrolment[14]
            returnObj["end_register"] = enrolment[15]
            returnObj["status"] = enrolment[16]

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
                "message":"Oops no self-enrolment request exists"
            }
        ),404

# Get all Self-Enrolment request by learner_id
def getLearnerSelfEnrolmentRequests(data):
    learnerId = data["learnerId"]
    enrolments = db.session.query(LMSEnrolment.learner_id, LMSEnrolment.conduct_id, LMSUser.name, LMSUser.email, LMSUser.seniority_level, LMSUser.contact, LMSCourse.course_id, LMSCourse.course_code, LMSCourse.title, LMSCourse.outline, LMSConduct.trainer_id, LMSConduct.capacity, LMSConduct.start_date, LMSConduct.end_date, LMSConduct.start_register, LMSConduct.end_register, LMSEnrolment.status, LMSEnrolment.remarks).filter(
        LMSUser.user_id == LMSEnrolment.learner_id, 
        LMSEnrolment.conduct_id == LMSConduct.conduct_id, 
        LMSConduct.course_id == LMSCourse.course_id, 
        or_(LMSEnrolment.status == "Request", LMSEnrolment.status == "Reject"), 
        LMSEnrolment.learner_id == learnerId).all()

    returnArray = []
    if enrolments:
        for enrolment in enrolments:
            returnObj = {}
            returnObj["learner_id"] = enrolment[0]
            returnObj["conduct_id"] = enrolment[1]
            returnObj["name"] = enrolment[2]
            returnObj["email"] = enrolment[3]
            returnObj["seniority_level"] = enrolment[4]
            returnObj["contact"] = enrolment[5]
            returnObj["course_id"] = enrolment[6]
            returnObj["course_code"] = enrolment[7]
            returnObj["title"] = enrolment[8]
            returnObj["outline"] = enrolment[9]
            returnObj["trainer_id"] = enrolment[10]
            returnObj["capacity"] = enrolment[11]
            returnObj["start_date"] = enrolment[12]
            returnObj["end_date"] = enrolment[13]
            returnObj["start_register"] = enrolment[14]
            returnObj["end_register"] = enrolment[15]
            returnObj["status"] = enrolment[16]
            returnObj["remarks"] = enrolment[17]

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
                "message":"Oops no self-enrolment request exists"
            }
        ),404

# Add new Enrolment
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

# Update Enrolment by learner_id and conduct_id
def updateEnrolment(data):
    if not all(key in data.keys() for
                key in ('learnerId', "conductId", "status", "remarks")):
                        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    learnerId = data["learnerId"]
    conductId = data["conductId"]
    enrolment = LMSEnrolment.query.filter_by(learner_id=learnerId, conduct_id=conductId).first()
    if not enrolment:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such enrolment was found"
        }),404
    else:
        localEnrolment = db.session.merge(enrolment)
        status = data["status"]
        remarks = data["remarks"]
        localEnrolment.status = status
        localEnrolment.remarks = remarks
        try:
            db.session.add(localEnrolment)
            db.session.commit()
            return jsonify({
                "code" : 200,
                "data" : localEnrolment.to_dict()
            }),200
        except Exception as e:
            print(str(e))
            return jsonify({
                "code" : 500,
                "message": "Unable to commit to database."
            }), 500


# Delete an Enrolment request by learner_id and conduct_id
def deleteEnrolment(data):
    learnerId = data['learnerId']
    conductId = data['conductId']
    enrolment = db.session.query(LMSEnrolment).filter(LMSEnrolment.learner_id == learnerId, LMSEnrolment.conduct_id == conductId).first()
    if enrolment:
        db.session.delete(enrolment)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": {
                    "learner_id": learnerId,
                    "conduct_id": conductId
                }
            }
        ), 200
    return jsonify(
        {
            "code": 404,
            "data": {
                "learner_id": learnerId,
                "conduct_id": conductId
            },
            "message": "Enrolment for this learner and conduct not found."
        }
    ), 404