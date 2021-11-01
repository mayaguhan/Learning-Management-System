from flask import Flask, request, jsonify
from ..data_access.classes import LMSQuizAttempt, LMSQuizChoice, LMSQuizPerformance, LMSQuizQuestion
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def getQuizPerformanceByQuizAttemptID(data):
    if not ("attemptId" in data.keys()):
                       return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    attemptId = data["attemptId"]
    quizPerformances = db.session.query(LMSQuizQuestion.quiz_question_id,LMSQuizQuestion.question_name,LMSQuizChoice.quiz_choice_id,
    LMSQuizChoice.quiz_question_id,LMSQuizChoice.choice,LMSQuizChoice.correct).filter(LMSQuizPerformance.quiz_choice_id==LMSQuizChoice.quiz_choice_id,LMSQuizQuestion.quiz_question_id==LMSQuizChoice.quiz_question_id,LMSQuizPerformance.quiz_attempt_id==attemptId).all()
    if not quizPerformances:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such performance data was found"
        }),404
    quizPerformancesFormatted = []
    for quizPerformance in quizPerformances:
        performance = {}
        performance["quiz_question_id"] = quizPerformance[0]
        performance["question_name"] = quizPerformance[1]
        performance["quiz_choice_id"] = quizPerformance[2]
        performance["choice"] = quizPerformance[4]
        performance["correct"] = quizPerformance[5]
        quizPerformancesFormatted.append(performance)
    return jsonify({
        "code" : 201,
        "data" : quizPerformancesFormatted
    }),201

def getQuizQuestionsAndChoicesBySectionId(data):
    if not ("sectionId" in data.keys()):
                       return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    sectionId = data["sectionId"]
    quizQuestions = db.session.query(LMSQuizQuestion.quiz_question_id,LMSQuizChoice.quiz_choice_id,LMSQuizQuestion.question_name,
    LMSQuizChoice.choice,LMSQuizChoice.correct).filter(LMSQuizQuestion.quiz_question_id==LMSQuizChoice.quiz_question_id,LMSQuizQuestion.section_id==sectionId).order_by(LMSQuizChoice.quiz_choice_id).all()
    if not quizQuestions:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such choice was found"
        }),404
    quizQuestionsFormatted = []
    for quizQuestion in quizQuestions:
        question = {}
        question["quiz_question_id"] = quizQuestion[0]
        question["quiz_choice_id"] = quizQuestion[1]
        question["question_name"] = quizQuestion[2]
        question["choice"] = quizQuestion[3]
        question["correct"] = quizQuestion[4]
        quizQuestionsFormatted.append(question)
    return jsonify({
        "code" : 201,
        "data" : quizQuestionsFormatted
    }),201

def getAllCorrectQuizChoicesBySectionId(data):
    if not ("sectionId" in data.keys()):
                       return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    sectionId = data["sectionId"]
    quizChoices = db.session.query(LMSQuizQuestion.quiz_question_id,LMSQuizQuestion.section_id,LMSQuizQuestion.question_name,LMSQuizChoice.quiz_choice_id,
    LMSQuizChoice.quiz_question_id,LMSQuizChoice.correct,LMSQuizChoice.correct).filter(LMSQuizQuestion.quiz_question_id==LMSQuizChoice.quiz_question_id,LMSQuizQuestion.section_id==sectionId,LMSQuizChoice.correcet==1).all()
    if not quizChoices:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such choice was found"
        }),404
    quizQuestionsFormatted = []
    for quizChoice in quizChoices:
        question = {}
        question["quiz_question_id"] = quizChoice[0]
        question["section_id"] = quizChoice[1]
        question["question_name"] = quizChoice[2]
        question["quiz_choice_id"] = quizChoice[3]
        question["choice"] = quizChoice[4]
        question["correct"] = quizChoice[5]
        quizQuestionsFormatted.append(question)
    return jsonify({
        "code" : 201,
        "data" : quizQuestionsFormatted
    }),201

def getQuizQuestionsBySectionId(data):
    if not ("sectionId" in data.keys()):
                       return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    sectionId = data["sectionId"]
    quizQuestions = db.session.query(LMSQuizQuestion.quiz_question_id,LMSQuizQuestion.question_name).filter(LMSQuizQuestion.section_id==sectionId).order_by(LMSQuizQuestion.quiz_question_id).all()
    if not quizQuestions:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such choice was found"
        }),404
    quizQuestionsFormatted = []
    for quizQuestion in quizQuestions:
        question = {}
        question["quiz_question_id"] = quizQuestion[0]
        question["question_name"] = quizQuestion[1]
        quizQuestionsFormatted.append(question)
    return jsonify({
        "code" : 201,
        "data" : quizQuestionsFormatted
    }),201

def updateQuizChoice(data):
    if not all(key in data.keys() for
                key in ('quizChoiceId', "choice","correct")):
                       return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    quizChoiceId = data["quizChoiceId"]
    quizChoice = LMSQuizChoice.query.filter_by(quiz_question_id=quizChoiceId).first()
    if not quizChoice:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such choice was found"
        }),404
    else:
        localQuizChoice = db.session.merge(quizChoice)
        choice = data["choice"]
        correct = data["correct"]
        localQuizChoice.choice = choice
        localQuizChoice.correct = correct
        try:
            db.session.add(localQuizChoice)
            db.session.commit()
            return jsonify({
                "code" : 200,
                "data" : localQuizChoice.to_dict()
            }),200
        except Exception as e:
            print(str(e))
            return jsonify({
                "code" : 500,
                "message": "Unable to commit to database."
            }), 500

def updateQuizQuestion(data):
    if not all(key in data.keys() for
                key in ('questionId', "questionName")):
                       return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    questionId = data["questionId"]
    quizQuestion = LMSQuizQuestion.query.filter_by(quiz_question_id=questionId).first()
    if not quizQuestion:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such question was found"
        }),404
    else:
        localQuestion = db.session.merge(quizQuestion)
        questionName = data["questionName"]
        localQuestion.question_name = questionName
        try:
            db.session.add(localQuestion)
            db.session.commit()
            return jsonify({
                "code" : 200,
                "data" : localQuestion.to_dict()
            }),200
        except Exception as e:
            print(str(e))
            return jsonify({
                "code" : 500,
                "message": "Unable to commit to database."
            }), 500

def addQuizAttempt(data):
    if not all(key in data.keys() for
                key in ('learnerId', "sectionId")):
                       return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    quizAttempt = LMSQuizAttempt()
    quizAttempt.learner_id = data["learnerId"]
    quizAttempt.section_id = data["sectionId"]
    try:
        db.session.add(quizAttempt)
        db.session.commit()
    except Exception as e:
        print(str(e))
        return jsonify({
            "code" : 500,
            "message" : "An error occurred creating the attempt record"
        }),500
    return jsonify(
        {
            "code": 201,
            "data": quizAttempt.to_dict()
        }
    ), 201

def addQuizPerformance(data):
    if not all(key in data.keys() for
                key in ('quizAttemptId', "questionId","quizChoiceId")):
                       return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    quizPerformance = LMSQuizPerformance(quiz_attempt_id=data["quizAttemptId"],quiz_question_id=data["questionId"],quiz_choice_id=data["quizChoiceId"])
    try:
        db.session.add(quizPerformance)
        db.session.commit()
    except Exception as e:
        print(str(e))
        return jsonify({
            "code" : 500,
            "message" : "An error occurred creating the attempt performance record"
        }),500
    return jsonify(
        {
            "code": 201,
            "data": quizPerformance.to_dict()
        }
    ), 201

def addQuizChoice(data):
    if not all(key in data.keys() for
                key in ('quizQuestionId', "choice", "correct")):
                       return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    choice = LMSQuizChoice(quiz_question_id=data["quizQuestionId"],choice=data["choice"],correct=data["correct"])
    try:
        db.session.add(choice)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "error" : str(e),
                "message": "An error occurred creating the choice."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": choice.to_dict()
        }
    ), 201


def addQuizQuestion(data):
    if not all(key in data.keys() for
                key in ('sectionId', "questionName")):
                       return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    question = LMSQuizQuestion(section_id=data["sectionId"],question_name=data["questionName"])
    try:
        db.session.add(question)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "error" : str(e),
                "message": "An error occurred creating the question."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": question.to_dict()
        }
    ), 201


# def getQuizAttempyByID(data):
#     quizAttemptID = data["attemptId"]
#     quiz_attempt = LMSQuizAttempt.query.filter_by(quiz_attempt_id=quizAttemptID).first()
#     if quiz_attempt:
#         return jsonify({
#             "code" : 200,
#             "data" : quiz_attempt.to_dict()
#         }),200
#     else:
#         return jsonify({
#             "code" : 404,
#             "message" : "Error, no such attempt was found"
#         }),404


def updateQuizAttemptGrade(data):
    grade = data["grade"]
    quizAttemptID = data["attemptId"]
    quiz_attempt = LMSQuizAttempt.query.filter_by(quiz_attempt_id=quizAttemptID).first()
    if not quiz_attempt:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such attempt was found"
        }),404
    else:
        quiz_attempt.grade=grade
        db.session.commit()
        return jsonify({
            "code" : 200,
            "data" : quiz_attempt.to_dict()
        }),200
    