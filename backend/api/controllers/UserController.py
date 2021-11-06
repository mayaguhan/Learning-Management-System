from flask import Flask, request, jsonify
from ..data_access.lms_user import LMSUser
from ..data_access.lms_conduct import LMSConduct
from ..data_access.lms_enrolment import LMSEnrolment
from ..data_access.lms_course import LMSCourse
from ..data_access.classes import LMSUser, LMSConduct, LMSCourse, LMSQuizAttempt, LMSSection
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

from ..data_access.lms_conduct import LMSConduct
from ..data_access.lms_enrolment import LMSEnrolment

db = SQLAlchemy()

# Login User by email
def retrieveUserIdByEmail(data):
    email = data["email"]
    user = LMSUser.query.filter_by(email=email).first()

    if user:
        return jsonify(
            {
                "code" : 200,
                "user_id": user.getUserId()  
            }
        ),200
    else:
        return jsonify(
            {
                "code" : 404,
                "message":"Oops no user with that email address exists"
            }
        ),404

# Get all Users
def getAllUsers():
    users = LMSUser.query.all()
    if users:
        return jsonify(
            {
                "code" : 200,
                "data":[user.to_dict() for user in users]
            }
        ),200
    else:
        return jsonify(
            {
                "code": 404,
                "message":"Oops no one exists"
            }
        ),404

# Get a single User
def getASingleUser(data):
    userId = data["userId"]
    users = db.session.query(LMSUser).filter(LMSUser.user_id == userId)

    if users:
        return jsonify(
            {
                "code" : 200,
                "data":[user.to_dict() for user in users]
            }
        ),200
    else:
        return jsonify(
            {
                "code": 404,
                "message":"Oops no one exists"
            }
        ),404

# Get all Users by seniority_level
def getUsersBySeniority(data):
    seniority_level = data["seniorityLevel"]
    users = LMSUser.query.filter_by(seniority_level=seniority_level)
    if users:
        return jsonify(
            {
                "code" : 200,
                "data":[user.to_dict() for user in users]
            }
        ),200
    else:
        return jsonify(
            {
                "code" : 404,
                "message":"Oops no one has that seniority level."
            }
        ),404

# Get all Users that has completed a Course by course_id
def getUsersThatHasCompletedACourse(data):
    courseId = data["courseId"]
    users = db.session.query(LMSUser).filter(LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSEnrolment.learner_id == LMSUser.user_id, LMSEnrolment.status == "Complete", LMSConduct.course_id == courseId).all()

    if users:
        return jsonify(
            {
                "code" : 200,
                "data":[user.to_dict() for user in users]
            }
        ),200
    else:
        return jsonify(
            {
                "code": 404,
                "message":"Oops no one has completed this course."
            }
        ),404

# Get all Engineers that are eligible for a course by course id
def getEngineersThatAreEligibleForACourse(data):
    courseId = data["courseId"]
    subQuery = db.session.query(LMSEnrolment.learner_id).filter(LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSConduct.course_id == courseId)
    users = db.session.query(LMSUser).filter(LMSUser.user_id.notin_(subQuery), LMSUser.seniority_level == "Engineer").all()
    # print(users)
    
    if users:
        return jsonify(
            {
                "data":[user.to_dict() for user in users],
                "code": 200
            }
        ),200
    else:
        return jsonify(
            {
                "code" : 404,
                "message":"Oops no one is eligible for this course."
            }
        ),404

# Get all Engineers that are eligible for a course with requisite by course id
def getEngineersThatAreEligibleForACourseWithPreReq(data):
    courseId = data["courseId"]

    courseReqQuery = db.session.query(LMSCourse.course_requisite_id).filter(LMSCourse.course_id == courseId)
    subQuery1 = db.session.query(LMSUser).filter(LMSUser.user_id == LMSEnrolment.learner_id, LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSUser.seniority_level == "Engineer", LMSEnrolment.status == "Complete", LMSConduct.course_id == courseReqQuery).all()
    queryRequiredForSubQuery2 = db.session.query(LMSEnrolment.learner_id).filter(LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSConduct.course_id == courseId)

    subQuery2 = db.session.query(LMSUser).filter(LMSUser.user_id.notin_(queryRequiredForSubQuery2), LMSUser.seniority_level == "Engineer").all()
    users = []

    if subQuery1 and subQuery2:
        for user in subQuery1:
            userId = user.getUserId()
            for user2 in subQuery2:
                if userId == user2.getUserId():
                    users.append(user)

    if len(users) > 0:
        return jsonify(
            {
                "code" : 200,
                "data":[user.to_dict() for user in users]
            }
        ),200
    else:
        return jsonify(
            {
                "code": 404,
                "message":"Oops no one is eligible this course."
            }
        ),404


# Get all Trainers eligible to teach a Course by course_id
def getTrainersThatAreEligibleToTeachACourse(data):
    courseId = data["courseId"]
    users = db.session.query(LMSUser).filter(LMSUser.user_id == LMSEnrolment.learner_id, LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSUser.seniority_level == "Senior Engineer", LMSEnrolment.status == "Complete", LMSConduct.course_id == courseId).all()
    print(users)

    if users:
        return jsonify(
            {
                "code": 200,
                "data":[user.to_dict() for user in users]
            }
        ),200
    else:
        return jsonify(
            {
                "code": 404,
                "message":"Oops no one is eligible for this course."
            }
        ),404

# Get all Trainers that are conducting a Course by course_id
def getTrainersConductingACourse(data):
    courseId = data["courseId"]

    enrolmentsSubquery = db.session.query(LMSEnrolment.conduct_id, (func.count(LMSEnrolment.learner_id)).label('enrolments')).filter(
        LMSConduct.conduct_id == LMSEnrolment.conduct_id).group_by(LMSConduct.course_id, LMSConduct.trainer_id).subquery()

    trainerList = db.session.query(LMSUser, LMSConduct, enrolmentsSubquery.c.enrolments).select_from(LMSConduct).join(
        enrolmentsSubquery, enrolmentsSubquery.c.conduct_id == LMSConduct.conduct_id, isouter=True).filter(
            LMSUser.user_id == LMSConduct.trainer_id, 
            LMSConduct.course_id == LMSCourse.course_id, 
            LMSConduct.start_register <= datetime.today(),
            LMSConduct.end_date >= datetime.today(),
            LMSUser.seniority_level == "Senior Engineer",
            LMSConduct.course_id == courseId).all()
    print(trainerList)
    returnArray = []
    if len(trainerList) > 0:
        for result in trainerList:
            user = result[0]
            conduct = result[1]
            enrolments = 0
            if (result[2] is not None):
                enrolments = result[2]

            returnObj = {}
            returnObj["conduct_id"] = conduct.getConductId()
            returnObj["course_id"] = conduct.getCourseId()
            returnObj["trainer_id"] = conduct.getTrainerId()
            returnObj["name"] = user.getName()
            returnObj["email"] = user.getEmail()
            returnObj["contact"] = user.getContact()
            returnObj["capacity"] = conduct.getCapacity()
            returnObj["start_date"] = conduct.getStartDate()
            returnObj["end_date"] = conduct.getEndDate()
            returnObj["start_register"] = conduct.getStartDate()
            returnObj["end_register"] = conduct.getEndDate()
            returnObj['enrolments'] = enrolments
            returnObj['remaining'] = conduct.getCapacity() - enrolments
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
                "message":"Oops no Trainer is eligible to teach this course."
            }
        ),404


# Get all Learners that are enrolled into a course by conduct_id
def getLearnersEnrolledByConduct(data):
    conductId = data["conductId"]
    sectionCount = len(db.session.query(LMSSection.section_id).filter(LMSSection.conduct_id == conductId).all())

    progressCount = db.session.query(LMSQuizAttempt.learner_id).filter(
        LMSQuizAttempt.section_id == LMSSection.section_id, 
        LMSQuizAttempt.grade >= LMSSection.passing_grade, 
        LMSSection.conduct_id == conductId).group_by(LMSQuizAttempt.learner_id, LMSQuizAttempt.section_id).subquery()

    learnerProgressSubquery = db.session.query(progressCount.c.learner_id, (func.count(progressCount.c.learner_id)).label('progress')).group_by(progressCount.c.learner_id).subquery()

    learnerList = db.session.query(LMSUser, LMSEnrolment, learnerProgressSubquery.c.progress).join(
        learnerProgressSubquery, learnerProgressSubquery.c.learner_id == LMSEnrolment.learner_id, isouter=True).filter(
            LMSUser.user_id == LMSEnrolment.learner_id, 
            LMSEnrolment.conduct_id == conductId).group_by(LMSEnrolment.learner_id).all()

    returnArray = []
    if len(learnerList) > 0:
        for result in learnerList:
            user = result[0]
            progress = 0
            if (result[2] is not None):
                progress = result[2]

            returnObj = {}
            returnObj["user_id"] = user.getUserId()
            returnObj["name"] = user.getName()
            returnObj["email"] = user.getEmail()
            returnObj["seniority_level"] = user.getSeniorityLevel()
            returnObj["contact"] = user.getContact()
            returnObj["progress"] = progress
            returnObj["section_count"] = sectionCount
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
                "message":"Oops no Learners is in this course."
            }
        ),404

# Add a new user
def addUser(data):
    user = LMSUser(**data)
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the user."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": user.to_dict()
        }
    ), 201