from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from ..data_access.lms_user import LMSUser
from ..data_access.lms_conduct import LMSConduct

from ..data_access.lms_enrolment import LMSEnrolment
from ..data_access.lms_course import LMSCourse


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

# Get a single course
def getASingleCourse(data):
    courseId = data["courseId"]
    course = db.session.query(LMSCourse).filter(LMSCourse.course_id == courseId).first()
    preRequisiteCourse = db.session.query(LMSCourse).filter(LMSCourse.course_id == course.getCourseRequisiteId()).first()

    returnArray = []

    if course:
        # Pre-requisite exists
        courseObj = {}

        if preRequisiteCourse:
            courseObj["course_id"] = course.getCourseId()
            courseObj["course_code"] = course.getCourseCode()
            courseObj["title"] = course.getTitle()
            courseObj["outline"] = course.getOutline()
            courseObj["badge"] = course.getBadge()
            courseObj["active"] = course.getActive()
            courseObj["course_requisite_id"] = course.getCourseRequisiteId()
            courseObj["cr_course_code"] = preRequisiteCourse.getCourseCode()
            courseObj["cr_title"] = preRequisiteCourse.getTitle()
            courseObj["cr_badge"] = course.getBadge()
            courseObj["cr_active"] = course.getActive()

        # No pre-requisite
        else:
            courseObj["course_id"] = course.getCourseId()
            courseObj["course_code"] = course.getCourseCode()
            courseObj["title"] = course.getTitle()
            courseObj["outline"] = course.getOutline()
            courseObj["badge"] = course.getBadge()
            courseObj["active"] = course.getActive()
            courseObj["course_requisite_id"] = course.getCourseRequisiteId()
            courseObj["cr_course_code"] = ""
            courseObj["cr_title"] = ""
            courseObj["cr_badge"] = ""
            courseObj["cr_active"] = ""
        
        returnArray.append(courseObj)

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
                "message":"Oops no course exists"
            }
        ),404

# Get all courses that a user has enrolled in
def getAllCoursesAUserHasEnrolled(data):
    learnerId = data["learnerId"]
    resultList = db.session.query(LMSCourse, LMSConduct, LMSEnrolment.status).filter(LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSCourse.course_id == LMSConduct.course_id, LMSEnrolment.learner_id == learnerId).order_by(LMSEnrolment.status.desc()).all()

    returnArray = []
    if len(resultList) > 0:
        for result in resultList:
            course = result[0]
            conduct = result[1]

            returnObj = {}
            returnObj["course_id"] = course.getCourseId()
            returnObj["course_requisite_id"] = course.getCourseRequisiteId()
            returnObj["course_code"] = course.getCourseCode()
            returnObj["title"] = course.getTitle()
            returnObj["outline"] = course.getOutline()
            returnObj["active"] = course.getActive()
            returnObj["conduct_id"] = conduct.getConductId()
            returnObj["trainer_id"] = conduct.getTrainerId()
            returnObj["capacity"] = conduct.getCapacity()
            returnObj["start_date"] = conduct.getStartDate()
            returnObj["end_date"] = conduct.getEndDate()
            returnObj["start_register"] = conduct.getStartRegister()
            returnObj["end_register"] = conduct.getEndRegister()
            returnObj["status"] = result[2]

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
                "message":"Oops no course exists"
            }
        ),404

# Get all courses that a user has completed by learner id
def getAllCompletedCoursesByUserId(data):
    userId = data["learnerId"]
    resultList = db.session.query(LMSUser.name, LMSConduct, LMSCourse).filter(LMSCourse.course_id == LMSConduct.course_id, LMSConduct.trainer_id == LMSUser.user_id, LMSEnrolment.conduct_id == LMSConduct.conduct_id, LMSEnrolment.learner_id == userId, LMSEnrolment.status == "Complete").group_by(LMSEnrolment.conduct_id).all()

    returnArray = []

    if len(resultList) > 0:
        for result in resultList:
            course = result[2]
            conduct = result[1]

            returnObj = {}
            returnObj["conduct_id"] = conduct.getConductId()
            returnObj["course_id"] = conduct.getCourseId()
            returnObj["course_requisite_id"] = course.getCourseRequisiteId()
            returnObj["course_code"] = course.getCourseCode()
            returnObj["title"] = course.getTitle()
            returnObj["outline"] = course.getOutline()
            returnObj["badge"] = course.getBadge()
            returnObj["start_date"] = conduct.getStartDate()
            returnObj["end_date"] = conduct.getEndDate()
            returnObj["trainer_id"] = conduct.getTrainerId()
            returnObj["name"] = result[0]

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
                "message":"Oops no course exists"
            }
        ),404


# Add a course
def addACourse(data):
    course = LMSCourse(**data)
    try:
        db.session.add(course)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the course."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": course.to_dict()
        }
    ), 201
