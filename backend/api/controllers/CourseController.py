from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from datetime import datetime

from ..data_access.lms_user import LMSUser
from ..data_access.lms_conduct import LMSConduct
from ..data_access.lms_enrolment import LMSEnrolment
from ..data_access.lms_course import LMSCourse
from ..data_access.classes import LMSQuizAttempt, LMSSection


db = SQLAlchemy()

# Get all courses
def getAllCourses():
    courseRequisiteAlias = aliased(LMSCourse)

    trainerSubquery = db.session.query(LMSCourse.course_id, (func.count(LMSConduct.trainer_id)).label('trainer_count')).join(
        LMSConduct, LMSConduct.course_id == LMSCourse.course_id, isouter=True).filter(
            LMSConduct.start_register <= datetime.today(),
            LMSConduct.end_register >= datetime.today()).group_by(LMSCourse.course_id).subquery()

    trainerAllSubquery = db.session.query(LMSConduct.course_id, (func.count(LMSConduct.trainer_id)).label('trainer_all')).filter(
        LMSConduct.start_register <= datetime.today(),
        LMSConduct.end_date >= datetime.today()).group_by(LMSConduct.course_id).subquery()

    courseList = db.session.query(LMSCourse, courseRequisiteAlias, trainerSubquery.c.trainer_count, trainerAllSubquery.c.trainer_all).join(
        trainerSubquery, trainerSubquery.c.course_id == LMSCourse.course_id, isouter=True).join(
            courseRequisiteAlias, courseRequisiteAlias.course_id == LMSCourse.course_requisite_id, isouter=True).join(
                trainerAllSubquery, trainerAllSubquery.c.course_id == LMSCourse.course_id, isouter=True).order_by(LMSCourse.active, LMSCourse.course_code).all()
    
    returnArray = []
    if len(courseList) > 0:
        for result in courseList:
            course = result[0]
            courseRequisite = result[1]
            trainer_count = 0
            trainer_progress = 0
            trainer_all = 0

            if result[2]:
                trainer_count = result[2]
            if result[3]:
                trainer_all = result[3]
                trainer_progress = trainer_all - trainer_count

            returnObj = {}

            returnObj["course_id"] = course.getCourseId()
            returnObj["course_code"] = course.getCourseCode()
            returnObj["title"] = course.getTitle()
            returnObj["outline"] = course.getOutline()
            returnObj["badge"] = course.getBadge()
            returnObj["active"] = course.getActive()
            returnObj['trainer_count'] = trainer_count
            returnObj['trainer_progress'] = trainer_progress
            returnObj['trainer_all'] = trainer_all

            if courseRequisite:
                returnObj["course_requisite_id"] = courseRequisite.getCourseId()
                returnObj["cr_course_code"] = courseRequisite.getCourseCode()
                returnObj["cr_title"] = courseRequisite.getTitle()
            else:
                returnObj["course_requisite_id"] = None
                returnObj["cr_course_code"] = None
                returnObj["cr_title"] = None

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
                "message":"Oops no no courses exist."
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

        courseObj["course_id"] = course.getCourseId()
        courseObj["course_code"] = course.getCourseCode()
        courseObj["title"] = course.getTitle()
        courseObj["outline"] = course.getOutline()
        courseObj["badge"] = course.getBadge()
        courseObj["active"] = course.getActive()

        if preRequisiteCourse:
            courseObj["course_requisite_id"] = course.getCourseRequisiteId()
            courseObj["cr_course_code"] = preRequisiteCourse.getCourseCode()
            courseObj["cr_title"] = preRequisiteCourse.getTitle()
            courseObj["cr_badge"] = course.getBadge()
            courseObj["cr_active"] = course.getActive()
        else:
            courseObj["course_requisite_id"] = None
            courseObj["cr_course_code"] = None
            courseObj["cr_title"] = None
            courseObj["cr_badge"] = None
            courseObj["cr_active"] = None

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

# Get a Single Course Conducted information by conduct_id
def getCourseConductInformation(data):
    courseRequisiteAlias = aliased(LMSCourse)

    conductId = data["conductId"]
    sectionCount = len(db.session.query(LMSSection.section_id).filter(LMSSection.conduct_id == conductId).all())

    enrolmentSubquery = db.session.query(LMSConduct.course_id, (func.count(LMSEnrolment.learner_id)).label('enrolments')).filter(
        LMSEnrolment.conduct_id == LMSConduct.conduct_id,
        or_(LMSEnrolment.status == "Progress", LMSEnrolment.status == "Complete"),
        LMSConduct.conduct_id == conductId).subquery()
    
    courseList = db.session.query(LMSCourse, LMSConduct, courseRequisiteAlias, enrolmentSubquery.c.enrolments).join(
        courseRequisiteAlias, courseRequisiteAlias.course_id == LMSCourse.course_requisite_id, isouter=True).filter(
            LMSCourse.course_id == LMSConduct.course_id, 
            LMSConduct.conduct_id == conductId).all()

    returnArray = []
    if len(courseList) > 0:
        for result in courseList:
            course = result[0]
            conduct = result[1]
            courseRequisite = result[2]

            returnObj = {}
            returnObj["course_id"] = course.getCourseId()
            returnObj["course_code"] = course.getCourseCode()
            returnObj["title"] = course.getTitle()
            returnObj["outline"] = course.getOutline()
            returnObj["badge"] = course.getBadge()
            returnObj["active"] = course.getActive()

            if courseRequisite:
                returnObj["course_requisite_id"] = course.getCourseRequisiteId()
                returnObj["cr_course_code"] = courseRequisite.getCourseCode()
                returnObj["cr_title"] = courseRequisite.getTitle()
                returnObj["cr_outline"] = courseRequisite.getOutline()
                returnObj["cr_badge"] = courseRequisite.getBadge()
                returnObj["cr_active"] = courseRequisite.getActive()
            else:
                returnObj["course_requisite_id"] = None
                returnObj["cr_course_code"] = None
                returnObj["cr_title"] = None
                returnObj["cr_outline"] = None
                returnObj["cr_badge"] = None
                returnObj["cr_active"] = None

            returnObj["start_date"] = conduct.getStartDate()
            returnObj["end_date"] = conduct.getEndDate()
            returnObj["start_register"] = conduct.getStartRegister()
            returnObj["end_register"] = conduct.getEndRegister()
            returnObj["capacity"] = conduct.getCapacity()
            returnObj["enrolments"] = result[3]
            returnObj['section_count'] = sectionCount
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
                "message":"Oops no no courses exist."
            }
        ),404

# Get all Courses a User has Enrolled
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

# Get all in-progress Courses a User has by learner_id
def getAllInProgressCoursesByUserId(data):
    learnerId = data["learnerId"]

    progressCountSubquery = db.session.query(LMSConduct.conduct_id, LMSSection.section_id, LMSQuizAttempt.learner_id).filter(
        LMSQuizAttempt.section_id == LMSSection.section_id,
        LMSConduct.conduct_id == LMSSection.conduct_id, 
        LMSQuizAttempt.grade >= LMSSection.passing_grade, 
        LMSQuizAttempt.learner_id == learnerId).group_by(LMSConduct.conduct_id, LMSSection.section_id).subquery()

    conductProgressSubquery = db.session.query((LMSConduct.conduct_id).label('conduct_id'), (func.count(progressCountSubquery.c.section_id)).label('progress')).join(
        progressCountSubquery, progressCountSubquery.c.conduct_id == LMSConduct.conduct_id, isouter=True).filter(
            LMSEnrolment.conduct_id == LMSConduct.conduct_id, 
            LMSEnrolment.learner_id == learnerId).group_by(LMSConduct.conduct_id).subquery()

    sectionCountSubquery = db.session.query(LMSConduct.conduct_id, LMSConduct.course_id, (func.count(LMSSection.section_id)).label('section_count')).filter(
        LMSConduct.conduct_id == LMSSection.conduct_id).group_by(LMSConduct.conduct_id, LMSConduct.trainer_id).subquery()

    courseList = db.session.query(LMSCourse, LMSConduct, LMSUser, conductProgressSubquery.c.progress, sectionCountSubquery.c.section_count).join(
        conductProgressSubquery, conductProgressSubquery.c.conduct_id == LMSConduct.conduct_id, isouter=True).filter(
            LMSCourse.course_id == LMSConduct.course_id, 
            LMSConduct.course_id == sectionCountSubquery.c.course_id,
            LMSConduct.trainer_id == LMSUser.user_id, 
            LMSEnrolment.conduct_id == LMSConduct.conduct_id, 
            LMSConduct.conduct_id == sectionCountSubquery.c.conduct_id,
            LMSEnrolment.status == "Progress",
            LMSConduct.start_date <= datetime.today(),
            LMSConduct.end_date >= datetime.today(),
            LMSEnrolment.learner_id == learnerId).group_by(LMSConduct.conduct_id).all()

    returnArray = []
    if len(courseList) > 0:
        for result in courseList:
            course = result[0]
            conduct = result[1]
            user = result[2]

            returnObj = {}
            
            returnObj["course_id"] = course.getCourseId()
            returnObj["course_requisite_id"] = course.getCourseRequisiteId()
            returnObj["course_code"] = course.getCourseCode()
            returnObj["title"] = course.getTitle()
            returnObj["outline"] = course.getOutline()
            returnObj["badge"] = course.getBadge()
            returnObj["trainer_id"] = user.getUserId()
            returnObj["name"] = user.getName()
            returnObj["conduct_id"] = conduct.getConductId()
            returnObj["start_date"] = conduct.getStartDate()
            returnObj["end_date"] = conduct.getEndDate()
            returnObj["start_register"] = conduct.getStartRegister()
            returnObj["end_register"] = conduct.getEndRegister()
            returnObj["capacity"] = conduct.getCapacity()
            returnObj["progress"] = result[3]
            returnObj['section_count'] = result[4]
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
                "message":"Oops no no courses exist."
            }
        ),404

# Get all completed Courses User has by learner_id
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

# Get all Courses a User has not Enrolled In
def getAllCoursesUserHasNotEnrolledIn(data):
    learnerId = data['learnerId']
    courseRequisiteAlias = aliased(LMSCourse)

    trainerSubquery = db.session.query(LMSCourse.course_id, LMSCourse.course_requisite_id, (func.count(LMSConduct.trainer_id)).label('trainer_count')).join(
        LMSConduct, LMSConduct.course_id == LMSCourse.course_id, isouter=True).filter(
            LMSConduct.start_register <= datetime.today(),
            LMSConduct.end_register >= datetime.today()).group_by(LMSCourse.course_id).subquery()

    enrolledCoursesSubquery = db.session.query(LMSConduct.course_id).filter(
        LMSConduct.conduct_id == LMSEnrolment.conduct_id,
        LMSConduct.course_id == LMSCourse.course_id,
        LMSEnrolment.learner_id == learnerId).subquery()

    courseList = db.session.query(LMSCourse, courseRequisiteAlias, trainerSubquery.c.trainer_count).join(
        trainerSubquery, trainerSubquery.c.course_id == LMSCourse.course_id, isouter=True).join(
            courseRequisiteAlias, courseRequisiteAlias.course_id == trainerSubquery.c.course_requisite_id, isouter=True).filter(
                LMSCourse.course_id.notin_(enrolledCoursesSubquery), 
                LMSCourse.active == 1).order_by(trainerSubquery.c.trainer_count.desc()).all()

    returnArray = []
    if len(courseList) > 0:
        for result in courseList:
            course = result[0]
            courseRequisite = result[1]

            returnObj = {}
            returnObj["course_id"] = course.getCourseId()
            returnObj["course_code"] = course.getCourseCode()
            returnObj["title"] = course.getTitle()
            returnObj["outline"] = course.getOutline()

            if courseRequisite:
                returnObj["course_requisite_id"] = course.getCourseRequisiteId()
                returnObj["cr_course_code"] = courseRequisite.getCourseCode()
                returnObj["cr_title"] = courseRequisite.getTitle()
            else:
                returnObj["course_requisite_id"] = None
                returnObj["cr_course_code"] = None
                returnObj["cr_title"] = None

            returnObj['trainer_count'] = result[2]
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
                "message":"Oops no no courses exist."
            }
        ),404

# Get all Courses that are conducted by trainer_id
def getAllCoursesConductedByTrainer(data):
    userId = data["trainerId"]
    resultList = db.session.query(LMSCourse, LMSConduct, LMSEnrolment, func.count(LMSEnrolment.learner_id)).filter(
        LMSCourse.course_id == LMSConduct.course_id, 
        LMSConduct.conduct_id == LMSEnrolment.conduct_id, 
        or_(LMSEnrolment.status == "Progress", LMSEnrolment.status == "Complete"),
        LMSConduct.trainer_id == userId).group_by(LMSConduct.conduct_id).all()

    returnArray = []

    if len(resultList) > 0:
        for result in resultList:
            course = result[0]
            conduct = result[1]

            returnObj = {}
            returnObj["course_id"] = course.getCourseId()
            returnObj["conduct_id"] = conduct.getConductId()
            returnObj["course_requisite_id"] = course.getCourseRequisiteId()
            returnObj["course_code"] = course.getCourseCode()
            returnObj["title"] = course.getTitle()
            returnObj["outline"] = course.getOutline()
            returnObj["badge"] = course.getBadge()
            returnObj["trainer_id"] = conduct.getTrainerId()
            returnObj["capacity"] = conduct.getCapacity()
            returnObj["start_date"] = conduct.getStartDate()
            returnObj["end_date"] = conduct.getEndDate()
            returnObj["start_register"] = conduct.getStartRegister()
            returnObj["end_register"] = conduct.getEndRegister()
            returnObj["enrolment"] = result[3]

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

# Update Course by course_id
def updateCourse(data):
    if not all(key in data.keys() for
                key in ("course_id", "course_requisite_id", "course_code", "title", "outline", "badge", "active")):
                        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    courseId = data["course_id"]
    course = LMSCourse.query.filter_by(course_id=courseId).first()
    if not course:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such course was found"
        }),404
    else:
        localCourse = db.session.merge(course)
        localCourse.course_requisite_id = data["course_requisite_id"]
        localCourse.course_code = data["course_code"]
        localCourse.title = data["title"]
        localCourse.outline = data["outline"]
        localCourse.badge = data["badge"]
        localCourse.active = data["active"]
        try:
            db.session.add(localCourse)
            db.session.commit()
            return jsonify({
                "code" : 200,
                "data" : localCourse.to_dict()
            }),200
        except Exception as e:
            print(str(e))
            return jsonify({
                "code" : 500,
                "message": "Unable to commit to database."
            }), 500

# Add new Course Conduct
def addCourseConduct(data):
    course = LMSConduct(**data)
    try:
        db.session.add(course)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the class."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": course.to_dict()
        }
    ), 201