from flask import Flask, request, jsonify
from sqlalchemy.sql.elements import Null
from ..data_access.lms_section_requirement import LMSSectionRequirement
from ..data_access.lms_section import LMSSection
from ..data_access.lms_material import LMSMaterial
from ..data_access.lms_material_visit import MaterialVisit
from ..data_access.lms_quiz_attempt import LMSQuizAttempt
from flask_sqlalchemy import SQLAlchemy

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

# def addNewMaterialVisit(data):
#     if not all(key in data.keys() for
#                key in ('learnerId', 'conductId',
#                        "materialId")):
#                        return jsonify({
#             "code" : 500,
#             "message" : "Error, inavlid input."
#         }),500
#     learnerId = data["learnerId"]
#     conductId = data["conductId"]
#     materialId = data["materialId"]
#     materialVisit = MaterialVisit()
#     materialVisit.learner_id = learnerId
#     materialVisit.material_id = materialId
#     material.link = link
#     try:
#         db.session.add(material)
#         db.session.commit()
#     except Exception as e:
#         print(str(e))
#         return jsonify(
#             {
#                 "code": 500,
#                 "message": "An error occurred creating the homework."
#             }
#         ), 500
#     return jsonify(
#         {
#             "code": 201,
#             "data": material.to_dict()
#         }
#     ), 201

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
    print(section.to_dict())
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
