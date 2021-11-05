from flask import Flask, request, jsonify
from sqlalchemy.sql.elements import Null

from ..data_access.lms_conduct import LMSConduct
from ..data_access.lms_enrolment import LMSEnrolment
from ..data_access.lms_section_requirement import LMSSectionRequirement
from ..data_access.lms_section import LMSSection
from ..data_access.lms_material import LMSMaterial 
from ..data_access.lms_material_visit import MaterialVisit 
from ..data_access.lms_quiz_attempt import LMSQuizAttempt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, case, or_

db = SQLAlchemy()


# Get all Sections by conduct_id and user_id (Learner)
def getAllSectionsByConductAndUserId(data):
    if not all(key in data.keys() for
                key in ('learnerId', 'conductId')):
                        return jsonify({
            "code" : 500,
            "message" : "Error, inavlid input."
        }),500
    learnerId = data["learnerId"]
    conductId = data["conductId"]
    # joinQuery = db.session.query(LMSQuizChoice,LMSQuizPerformance).join(LMSQuizPerformance,LMSQuizPerformance.quiz_choice_id==LMSQuizChoice.quiz_choice_id).filter(LMSQuizPerformance.quiz_attempt_id==quizAttemptId)#.all()
    # .filter(LMSQuizQuestion.quiz_question_id==LMSQuizChoice.quiz_question_id,LMSQuizPerformance.quiz_attempt_id==quizAttemptId,LMSQuizQuestion.section_id==sectionId)
    sections = db.session.query(
        LMSSection.section_id,
        LMSSection.section_name,
        LMSSection.sequence,
        LMSSection.quiz_duration,
        LMSSection.passing_grade,
        func.max(LMSQuizAttempt.grade),
        LMSMaterial.material_id,
        LMSMaterial.file_name, 
        LMSMaterial.link
        ).select_from(LMSSection).join(LMSQuizAttempt,LMSSection.section_id==LMSQuizAttempt.section_id,isouter=True).join(LMSMaterial,LMSMaterial.section_id==LMSSection.section_id,isouter=True).filter(LMSSection.conduct_id==conductId,LMSEnrolment.learner_id==learnerId).group_by(LMSSection.section_id, LMSMaterial.material_id).order_by(LMSSection.sequence).all()
    if not sections:
        return jsonify({
            "code" : 404,
            "message" : "Error, no quiz attempts were found"
        }),404
    else:
        returnArray = []
        for section in sections:
            individual = {}
            individual["section_id"] = section[0]
            individual["section_name"] = section[1]
            individual["sequence"] = section[2]
            individual["quiz_duration"] = section[3]
            individual["passing_grade"] = section[4]
            individual["best_grade"] =section[5]
            individual["material_id"] = section[6]
            individual["file_name"] = section[7]
            individual["link"] = section[8]
            # float(quizAttempt[2])
            returnArray.append(individual)
        print(returnArray)
        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201


# Get all Sections by conduct_id (Trainer)
def getAllSectionsByConductId(data):
    if not ("conductId" in data.keys()):
                        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    conductId = data["conductId"]
    passCountSubquery = db.session.query(LMSQuizAttempt.section_id).filter(
        LMSQuizAttempt.section_id==LMSSection.section_id,
        LMSQuizAttempt.grade>=LMSSection.passing_grade).group_by(LMSQuizAttempt.learner_id,LMSQuizAttempt.section_id).subquery()
    
    learnerCount = len(db.session.query(LMSEnrolment.learner_id).filter(
        or_(LMSEnrolment.status=="Pending",LMSEnrolment.status=="Complete"),
        LMSEnrolment.conduct_id==conductId).all())

    sectionCount = len(db.session.query(LMSSection.section_id).filter(LMSSection.conduct_id == conductId).all())

    sectionsInformation = db.session.query(LMSSection, LMSMaterial, func.count(passCountSubquery.c.section_id)).join(
        passCountSubquery, passCountSubquery.c.section_id==LMSSection.section_id, isouter=True).join(
            LMSMaterial, LMSMaterial.section_id==LMSSection.section_id).filter(
                LMSSection.conduct_id==conductId).group_by(
                    LMSSection.section_id, LMSMaterial.material_id).order_by(LMSSection.sequence).all()

    if not sectionsInformation:
        return jsonify({
            "code" : 404,
            "message" : "Error, no sections were found"
        }),404
    else:
        returnArray = []
        for result in sectionsInformation:
            individual = {}
            section = result[0]
            material = result[1]

            individual["section_id"] = section.getSectionID()
            individual["section_name"] = section.getSectionName()
            individual["sequence"] = section.getSequence()
            individual["quiz_duration"] = section.getQuizDuration()
            individual["passing_grade"] = section.getPassingGrade()
            individual["material_id"] = material.getMaterialID()
            individual["file_name"] = material.getFileName()
            individual["link"] = material.getLink()
            individual["pass_count"] = result[2]
            individual["section_count"] = sectionCount
            individual["learner_count"] = learnerCount

            returnArray.append(individual)
        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201

# Get Section information by section_id
def getSectionInformationBySectionId(data):
    if not ("sectionId" in data.keys()):
                    return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    sectionId = data["sectionId"]
    subQuery = db.session.query(LMSSection.section_id,func.count(LMSEnrolment.learner_id).label("enrolments")).filter(LMSEnrolment.conduct_id==LMSConduct.conduct_id,LMSConduct.conduct_id==LMSSection.conduct_id,LMSSection.section_id==sectionId, or_(LMSEnrolment.status == "Progress", LMSEnrolment.status == "Complete")).subquery()
    sections = db.session.query(LMSSection.conduct_id,LMSSection.sequence,LMSSection.section_name,LMSSection.quiz_duration,LMSSection.passing_grade,subQuery.c.enrolments).select_from(LMSSection).join(subQuery,subQuery.c.section_id==LMSSection.section_id).filter(LMSSection.section_id==sectionId)
    if not sections:
        return jsonify({
            "code" : 404,
            "message" : "Error, no sections were found"
        }),404
    else:
        returnArray = []
        for section in sections:
            individual = {}
            individual["conduct_id"] = section[0]
            individual["sequence"] = section[1]
            individual["section_name"] = section[2]
            individual["quiz_duration"] = section[3]
            individual["passing_grade"] = section[4]
            individual["enrolments"] =section[5]
            returnArray.append(individual)
        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201

# Add new Section
def addNewSection(data):
    course = LMSSection(**data)
    try:
        db.session.add(course)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the section."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": course.to_dict()
        }
    ), 201


# Update Section by section_id
def updateSectionBySectionID(data):
    if not all(key in data.keys() for
                key in ('section_id', 'section_name',
                        'sequence', 'quiz_duration',"passing_grade")):
                        return jsonify({
            "code" : 500,
            "message" : "Error, inavlid input."
        }),500
    sectionId = data["section_id"]
    section = LMSSection.query.filter_by(section_id=sectionId).first()
    if not section:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such section was found"
        }),404
    else:
        try:
            localSection = db.session.merge(section)
            localSection.section_name = data["section_name"]
            localSection.sequence = data["sequence"]
            localSection.quiz_duration = data["quiz_duration"]
            localSection.passing_grade = data["passing_grade"]

            db.session.add(localSection)
            db.session.commit()

            return jsonify({
                "code" : 200,
                "data" : localSection.to_dict()
            }),200
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500

# Update all course section's passing grade by section_id
def updateSectionPassingGrade(data):
    section_id = data["section_id"]
    section = LMSSection.query.filter_by(section_id=section_id).first()
    if not section:
        return jsonify({
            "code" : 404,
            "message" : "Error, no section attempt was found"
        }),404
    else:
        localSectionFinal = db.session.merge(section)
        localSectionFinal.passing_grade = 85
        db.session.add(localSectionFinal)
        db.session.commit()

        conduct_id = data["conduct_id"]
        sections = LMSSection.query.filter(LMSSection.conduct_id==conduct_id, LMSSection.section_id!=section_id).all()

        if sections:
            for updateSection in sections:
                localSection = db.session.merge(updateSection)
                localSection.passing_grade = 0
                db.session.add(localSection)
                db.session.commit()

        return jsonify({
            "code" : 200,
            "data" : section.to_dict()
        }),200



# Delete Section by section_id
def deleteSectionBySectionID(data):
    sectionId = data["sectionId"]
    section = LMSSection.query.filter_by(section_id=sectionId).first()
    if not section:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such section was found"
        }),404
    else:
        try:
            localSection = db.session.merge(section)
            db.session.delete(localSection)
            db.session.commit()
            return jsonify({
                "code" : 200,
                "data" : "Deletion successful"
            }),200
        except Exception as e:
            print(str(e))
            return jsonify({
                "code" : 500,
                "message": "Unable to commit to database."
            }), 500

# Add new Material
def addNewMaterial(data):
    if not all(key in data.keys() for
               key in ('sectionId', 'fileName',
                       "link")):
                       return jsonify({
            "code" : 500,
            "message" : "Error, inavlid input."
        }),500
    sectionId = data["sectionId"]
    fileName = data["fileName"]
    link = data["link"]
    material = LMSMaterial()
    material.section_id = sectionId
    material.file_name = fileName
    material.link = link
    try:
        db.session.add(material)
        db.session.commit()
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the homework."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": material.to_dict()
        }
    ), 201

# Get all Materials by section_id
def getMaterialsBySectionID(data):
    if not ("sectionId" in data.keys()):
                    return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    sectionId = data["sectionId"]
    materials = db.session.query(LMSMaterial.material_id,LMSMaterial.file_name,LMSMaterial.link).filter(LMSSection.section_id==LMSMaterial.section_id,LMSSection.section_id==sectionId).all()
    if not materials:
        return jsonify({
            "code" : 400,
            "message" : "No such material exists"
        }),400
    else:
        returnArray = []
        for material in materials:
            individual = {}
            individual["material_id"] = material[0]
            individual["file_name"] = material[1]
            individual["link"] = material[2]
            returnArray.append(individual)
        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201

# Get all Section Material by course_id
def getMaterialByCourseId(data):
    if not ("courseId" in data.keys()):
                    return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    courseId = data["courseId"]
    materials = db.session.query(LMSSection.section_id,LMSSection.section_name,LMSSection.sequence,LMSMaterial.material_id,LMSMaterial.file_name,LMSMaterial.link).filter(
        LMSSection.section_id==LMSMaterial.section_id,
        LMSConduct.course_id==courseId).all()
    if not materials:
        return jsonify({
            "code" : 400,
            "message" : "No such material exists"
        }),400
    else:
        returnArray = []
        for material in materials:
            individual = {}
            individual["section_id"] = material[0]
            individual["section_name"] = material[1]
            individual["sequence"] = material[2]
            individual["material_id"] = material[3]
            individual["file_name"] = material[4]
            individual["link"] = material[5]
            returnArray.append(individual)
        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201


# Delete Material by material_id
def deleteMaterialByMaterialID(data):
    materialId = data["materialId"]
    material = LMSMaterial.query.filter_by(material_id=materialId).first()
    print(material)
    if not material:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such material was found"
        }),404
    else:
        try:
            localMaterial = db.session.merge(material)
            db.session.delete(localMaterial)
            db.session.commit()
            return jsonify({
                "code" : 200,
                "data" : "Deletion successful"
            }),200
        except Exception as e:
            print(str(e))
            return jsonify({
                "code" : 500,
                "error" : str(e),
                "message": "Unable to commit to database."
            }), 500

# Add new Visited Material
def addNewMaterialVisit(data):
    if not all(key in data.keys() for
                key in ('learnerId', 'conductId',
                        "materialId")):
                        return jsonify({
            "code" : 500,
            "message" : "Error, inavlid input."
        }),500
    learnerId = data["learnerId"]
    conductId = data["conductId"]
    materialId = data["materialId"]
    materialVisit = MaterialVisit()
    materialVisit.learner_id = learnerId
    materialVisit.material_id = materialId
    materialVisit.conduct_id = conductId
    try:
        db.session.add(materialVisit)
        db.session.commit()
    except Exception as e:
        print(str(e))
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the homework."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": materialVisit.to_dict()
        }
    ), 201