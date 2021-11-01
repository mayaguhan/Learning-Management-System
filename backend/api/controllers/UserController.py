from flask import Flask, request, jsonify
from ..data_access.classes import LMSUser, LMSConduct, LMSEnrolment, LMSCourse
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Retrieve All Users

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

# Retrieve a single user
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



# Retrieve users by seniority level

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


# Retrieve User ID By Email

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

# Get all users that has completed a course by course id

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

# Get all engineers that are eligible for a course by course id
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

# Get all engineers that are eligible for a course with requisite by course Id
def getEngineersThatAreEligibleForACourseWithPreReq(data):
    courseId = data["courseId"]
    
    # Split query into parts
    courseReqQuery = db.session.query(LMSCourse.course_requisite_id).filter(LMSCourse.course_id == courseId)

    subQuery1 = db.session.query(LMSUser).filter(LMSUser.user_id == LMSEnrolment.learner_id, LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSUser.seniority_level == "Engineer", LMSEnrolment.status == "Complete", LMSConduct.course_id == courseReqQuery).all()


    queryRequiredForSubQuery2 = db.session.query(LMSEnrolment.learner_id).filter(LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSConduct.course_id == courseId)

    subQuery2 = db.session.query(LMSUser).filter(LMSUser.user_id.notin_(queryRequiredForSubQuery2), LMSUser.seniority_level == "Engineer").all()

    users = []

    # print(subQuery1)
    # print(subQuery2)


    # Not sure if there is any better way to do how YQ did it. This is the current way. Complexity is O(N**2) but I don't think there will be a performance issue as our data is quite small and O(N**2) is relatively fast.  I would still prefer to find a better way where we can just make use of SQLAlchemy but for now, this will suffice
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


# Get all trainers that are eligible to teach a course by course_id
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
                "message": "An error occurred creating the homework."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": user.to_dict()
        }
    ), 201