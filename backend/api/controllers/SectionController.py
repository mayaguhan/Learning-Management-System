from flask import Flask, request, jsonify
from sqlalchemy.sql.elements import Null
from ..data_access.classes import LMSEnrolment, LMSSectionRequirement, LMSSection, LMSMaterial, MaterialVisit, LMSQuizAttempt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, case

db = SQLAlchemy()

# def getAllSectionsByConductID(data):
#     if not all(key in data.keys() for
#                key in ("conductId")):
#                        return jsonify({
#             "code" : 500,
#             "message" : "Error, inavlid input."
#         }),500
#     conductId = data["conductId"]
#     pcQuery = db.session.query(LMSQuizAttempt.section_id==LMSSection.section_id,LMSQuizAttempt.grade>=LMSSection.passing_grade).group_by(LMSQuizAttempt.learner_id,LMSQuizAttempt.section_id)
#     thirdQuery = LMSSection.join(pcQuery)

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
        case(
            [
                (func.isnull(LMSQuizAttempt.grade),"No Attempt"),
                (func.max(LMSQuizAttempt.grade)>=LMSSection.passing_grade,"Pass")
            ],
            else_="Fail"
        )
        ).select_from(LMSSection).join(LMSQuizAttempt,LMSSection.section_id==LMSQuizAttempt.section_id).filter(LMSSection.conduct_id==conductId,LMSEnrolment.learner_id==learnerId).group_by(LMSSection.section_id).order_by(LMSSection.sequence).all()
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
            individual["result"] = section[6]
            # float(quizAttempt[2])
            returnArray.append(individual)
        print(returnArray)
        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201

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
    return jsonify({
            "code" : 200,
            "message" : materials
        }),500

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


def updateSectionBySectionID(data):
    if not all(key in data.keys() for
               key in ('sectionId', 'section_name',
                       'sequence', 'quiz_duration',"passing_grade")):
                       return jsonify({
            "code" : 500,
            "message" : "Error, inavlid input."
        }),500
    sectionId = data["sectionId"]
    section = LMSSection.query.filter_by(section_id=sectionId).first()
    if not section:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such section was found"
        }),404
    else:
        try:
            sectionName = data["section_name"]
            sequence = data["sequence"]
            quizDuration = data["quiz_duration"]
            passingGrade = data["passing_grade"]
            section.section_name = sectionName
            section.sequence = sequence
            section.quiz_duration = quizDuration
            section.passing_grade = passingGrade
            db.session.commit()
            return jsonify({
                "code" : 200,
                "data" : section.to_dict()
            }),200
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500
