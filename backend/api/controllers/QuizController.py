from flask import Flask, request, jsonify
from ..data_access.lms_quiz_attempt import LMSQuizAttempt
from ..data_access.lms_quiz_choice import LMSQuizChoice
from ..data_access.lms_quiz_performance import LMSQuizPerformance
from ..data_access.lms_quiz_question import LMSQuizQuestion
from ..data_access.lms_section import LMSSection
from ..data_access.lms_user import LMSUser
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, case, and_
import json

db = SQLAlchemy()

# Get all Quiz Attempt by section_id
def getQuizAttemptForSection(data):
    if not("sectionId" in data.keys()):
        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    sectionId = data["sectionId"]
    # joinQuery = db.session.query(LMSQuizChoice,LMSQuizPerformance).join(LMSQuizPerformance,LMSQuizPerformance.quiz_choice_id==LMSQuizChoice.quiz_choice_id).filter(LMSQuizPerformance.quiz_attempt_id==quizAttemptId)#.all()
    # .filter(LMSQuizQuestion.quiz_question_id==LMSQuizChoice.quiz_question_id,LMSQuizPerformance.quiz_attempt_id==quizAttemptId,LMSQuizQuestion.section_id==sectionId)
    quizAttempt = db.session.query(
        LMSUser.user_id,
        LMSUser.name,
        LMSUser.email,
        LMSUser.seniority_level,
        LMSUser.contact,
        LMSQuizAttempt.quiz_attempt_id,
        LMSQuizAttempt.grade,
            case(

                [(LMSQuizAttempt.grade>=LMSSection.passing_grade,"Pass")],
                else_="Fail"
            ),
        LMSQuizAttempt.attempt_date
        ).filter(LMSSection.section_id==LMSQuizAttempt.section_id,LMSQuizAttempt.learner_id==LMSUser.user_id,LMSQuizAttempt.section_id==sectionId).all()
    if not quizAttempt:
        return jsonify({
            "code" : 404,
            "message" : "Error, no quiz attempts were found"
        }),404
    else:
        returnArray = []
        for quizAttempt in quizAttempt:
            individual = {}
            individual["user_id"] = quizAttempt[0]
            individual["name"] = quizAttempt[1]
            individual["email"] = quizAttempt[2]
            individual["seniority_level"] = quizAttempt[3]
            individual["contact"] = str(quizAttempt[4])
            individual["quiz_attempt_id"] =quizAttempt[5]
            individual["grade"] = quizAttempt[6]
            individual["result"] = quizAttempt[7]
            individual["attempt_date"] = quizAttempt[8]
            # float(quizAttempt[2])
            returnArray.append(individual)
        print(returnArray)
        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201

# Get Quiz Attempt of each student who had taken the quiz by section_id
def getStudentQuizAttemptBySectionId(data):
    if not("sectionId" in data.keys()):
        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    sectionId = data["sectionId"]
    # joinQuery = db.session.query(LMSQuizChoice,LMSQuizPerformance).join(LMSQuizPerformance,LMSQuizPerformance.quiz_choice_id==LMSQuizChoice.quiz_choice_id).filter(LMSQuizPerformance.quiz_attempt_id==quizAttemptId)#.all()
    # .filter(LMSQuizQuestion.quiz_question_id==LMSQuizChoice.quiz_question_id,LMSQuizPerformance.quiz_attempt_id==quizAttemptId,LMSQuizQuestion.section_id==sectionId)
    quizAttempt = db.session.query(
        LMSQuizAttempt.learner_id,
        LMSUser.name,
        LMSUser.email,
        LMSUser.seniority_level,
        LMSUser.contact,
        func.sum(
            case(

                [(LMSQuizAttempt.grade>=LMSSection.passing_grade,1)],
                else_=0
            )
        ),
        func.count(LMSQuizAttempt.quiz_attempt_id),
        func.max(LMSQuizAttempt.grade)
        ).filter(LMSSection.section_id==LMSQuizAttempt.section_id,LMSQuizAttempt.learner_id==LMSUser.user_id,LMSQuizAttempt.section_id==sectionId).group_by(LMSQuizAttempt.learner_id).all()
    if not quizAttempt:
        return jsonify({
            "code" : 404,
            "message" : "Error, no quiz attempts were found"
        }),404
    else:
        returnArray = []
        for quizAttempt in quizAttempt:
            individual = {}
            individual["user_id"] = quizAttempt[0]
            individual["name"] = quizAttempt[1]
            individual["email"] = quizAttempt[2]
            individual["seniority_level"] = quizAttempt[3]
            individual["contact"] = str(quizAttempt[4])
            individual["pass_attempts"] = float(quizAttempt[5])
            individual["quiz_attempt"] = float(quizAttempt[6])
            individual["best_grade"] = float(quizAttempt[7])
            # float(quizAttempt[2])
            returnArray.append(individual)
        print(returnArray)
        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201

# Get Quiz Attempt passing rate and attempt count by section_id
def getQuizAttemptPassingRateBySectionId(data):
    if not("sectionId" in data.keys()):
        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    sectionId = data["sectionId"]
    # joinQuery = db.session.query(LMSQuizChoice,LMSQuizPerformance).join(LMSQuizPerformance,LMSQuizPerformance.quiz_choice_id==LMSQuizChoice.quiz_choice_id).filter(LMSQuizPerformance.quiz_attempt_id==quizAttemptId)#.all()
    # .filter(LMSQuizQuestion.quiz_question_id==LMSQuizChoice.quiz_question_id,LMSQuizPerformance.quiz_attempt_id==quizAttemptId,LMSQuizQuestion.section_id==sectionId)
    quizAttempt = db.session.query(
        func.sum(
            case(

                [(LMSQuizAttempt.grade>=LMSSection.passing_grade,1)],
                else_=0
            )
        ),
        func.count(LMSQuizAttempt.quiz_attempt_id),
        func.sum(
            case(
                [(LMSQuizAttempt.grade>=LMSSection.passing_grade,1)],
                else_=0
            )
        )/func.count(LMSQuizAttempt.quiz_attempt_id)
        ).filter(LMSSection.section_id==LMSQuizAttempt.section_id,LMSQuizAttempt.section_id==sectionId).all()
    if not quizAttempt:
        return jsonify({
            "code" : 404,
            "message" : "Error, no quiz attempts were found"
        }),404
    else:
        returnArray = []
        for quizAttempt in quizAttempt:
            individual = {}
            individual["pass_count"] = float(quizAttempt[0])
            individual["total_attempt"] = quizAttempt[1]
            individual["pass_rate"] = float(quizAttempt[2])
            returnArray.append(individual)
        print(returnArray)
        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201

# Get Quiz's Question Performance by section_id
def getQuizQuestionPerformanceBySectionId(data):
    if not("sectionId" in data.keys()):
        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    sectionId = data["sectionId"]

    # joinQuery = db.session.query(LMSQuizChoice,LMSQuizPerformance).join(LMSQuizPerformance,LMSQuizPerformance.quiz_choice_id==LMSQuizChoice.quiz_choice_id).filter(LMSQuizPerformance.quiz_attempt_id==quizAttemptId)#.all()
    # .filter(LMSQuizQuestion.quiz_question_id==LMSQuizChoice.quiz_question_id,LMSQuizPerformance.quiz_attempt_id==quizAttemptId,LMSQuizQuestion.section_id==sectionId)
    quizPerformances = db.session.query(LMSQuizQuestion, LMSQuizChoice, func.count(LMSQuizPerformance.quiz_choice_id)).select_from(LMSQuizQuestion).join(
        LMSQuizChoice,LMSQuizChoice.quiz_question_id==LMSQuizQuestion.quiz_question_id , isouter=True).join(
            LMSQuizPerformance,LMSQuizPerformance.quiz_choice_id==LMSQuizChoice.quiz_choice_id, isouter=True).filter(
                LMSQuizQuestion.section_id==sectionId).group_by(
                    LMSQuizChoice.quiz_choice_id).order_by(
                        LMSQuizQuestion.quiz_question_id,LMSQuizChoice.quiz_choice_id).all()
    if not quizPerformances:
        return jsonify({
            "code" : 404,
            "message" : "Error, no quiz performances were found"
        }),404
    else:
        returnArray = []
        for quizPerformance in quizPerformances:
            individual = {}
            question = quizPerformance[0]
            choice = quizPerformance[1]
            individual["quiz_question_id"] = question.getQuestionID()
            individual["question_name"] = question.getQuestionName()
            individual["quiz_choice_id"] = choice.getChoiceID()
            individual["choice"] = choice.getChoice()
            individual["correct"] = choice.getCorrect()
            individual["answer_count"] = quizPerformance[2]
            returnArray.append(individual)

        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201

# Get Learner's Quiz Performance by section_id
def getQuizPerformanceByQuizAtemptAndSectionId(data):
    if not all(key in data.keys() for
                key in ('sectionId', "attemptId")):
                        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    quizAttemptId = data["attemptId"]
    sectionId = data["sectionId"]
    # joinQuery = db.session.query(LMSQuizChoice,LMSQuizPerformance).join(LMSQuizPerformance,LMSQuizPerformance.quiz_choice_id==LMSQuizChoice.quiz_choice_id).filter(LMSQuizPerformance.quiz_attempt_id==quizAttemptId)#.all()
    # .filter(LMSQuizQuestion.quiz_question_id==LMSQuizChoice.quiz_question_id,LMSQuizPerformance.quiz_attempt_id==quizAttemptId,LMSQuizQuestion.section_id==sectionId)
    quizPerformances = db.session.query(LMSQuizQuestion.quiz_question_id,LMSQuizQuestion.question_name,LMSQuizChoice.quiz_choice_id,LMSQuizChoice.choice,LMSQuizPerformance.quiz_choice_id,LMSQuizChoice.correct).select_from(LMSQuizChoice).join(LMSQuizPerformance,and_(LMSQuizChoice.quiz_choice_id==LMSQuizPerformance.quiz_choice_id,LMSQuizPerformance.quiz_attempt_id==quizAttemptId),isouter=True).filter(LMSQuizQuestion.quiz_question_id==LMSQuizChoice.quiz_question_id,LMSQuizQuestion.section_id==sectionId).order_by(LMSQuizQuestion.quiz_question_id).all()
    if not quizPerformances:
        return jsonify({
            "code" : 404,
            "message" : "Error, no quiz performances were found"
        }),404
    else:
        returnArray = []
        for quizPerformance in quizPerformances:
            individual = {}
            individual["quiz_question_id"] = quizPerformance[0]
            individual["question_name"] = quizPerformance[1]
            individual["quiz_choice_id"] = quizPerformance[2]
            individual["choice"] = quizPerformance[3]
            individual["chosen"] = quizPerformance[4]
            individual["correct"] = quizPerformance[5]
            returnArray.append(individual)

        return jsonify({
                "code" : 201,
                "data" : returnArray
                }),201

# Add new Quiz Question
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

# Add new Quiz Choice
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

# Update Quiz Question by quiz_question_id
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

# Update Quiz Choice by quiz_choice_id
def updateQuizChoice(data):
    if not all(key in data.keys() for
                key in ('quizChoiceId', "choice","correct")):
                        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    quizChoiceId = data["quizChoiceId"]
    quizChoice = LMSQuizChoice.query.filter_by(quiz_choice_id=quizChoiceId).first()
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

# Delete Quiz Question by quiz_question_id
def deleteQuizQuestionByID(data):
    if not("questionId" in data.keys()):
        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    questionId = data["questionId"]

    # Check whether quiz question exists
    quizQuestion = LMSQuizQuestion.query.filter_by(quiz_question_id=questionId).all()
    if not quizQuestion:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such quiz question was found"
        }),404
    else:
        try:
            # delete quiz performance first due to foreign key dependence
            quizPerformance = LMSQuizPerformance.query.filter_by(quiz_question_id=questionId).all()
            if quizPerformance:
                try:
                    for performance in quizPerformance:
                        localPerformance = db.session.merge(performance)
                        db.session.delete(localPerformance)
                        db.session.commit()
                        
                except Exception as e:
                    print(str(e))
                    return jsonify({
                        "code" : 500,
                        "error" : str(e),
                        "message": "Unable to commit to database."
                    }), 500

            # delete quiz choice second due to foreign key dependence
            quizChoice = LMSQuizChoice.query.filter_by(quiz_question_id=questionId).all()
            if quizChoice:
                try:
                    for choice in quizChoice:
                        localChoice = db.session.merge(choice)
                        db.session.delete(localChoice)
                        db.session.commit()
                        
                except Exception as e:
                    print(str(e))
                    return jsonify({
                        "code" : 500,
                        "error" : str(e),
                        "message": "Unable to commit to database."
                    }), 500

            for question in quizQuestion:
                localQuestion = db.session.merge(question)
                db.session.delete(localQuestion)
                db.session.commit()
                
        except Exception as e:
            print(str(e))
            return jsonify({
                "code" : 500,
                "error" : str(e),
                "message": "Unable to commit to database."
            }), 500
        return jsonify({
                "code" : 201,
                "message": "Deletion Successful."
            }), 201

# Delete Quiz Choice by quiz_choice_id
def deleteQuizChoiceByID(data):
    if not("quizChoiceId" in data.keys()):
        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    quizChoiceId = data["quizChoiceId"]

    quizChoice = LMSQuizChoice.query.filter_by(quiz_choice_id=quizChoiceId).all()
    if not quizChoice:
        return jsonify({
            "code" : 404,
            "message" : "Error, no such quiz choice was found"
        }),404
    else:
        try:
            # delete quiz performance first due to foreign key dependence
            quizPerformance = LMSQuizPerformance.query.filter_by(quiz_choice_id=quizChoiceId).all()
            if quizPerformance:
                try:
                    for performance in quizPerformance:
                        localPerformance = db.session.merge(performance)
                        db.session.delete(localPerformance)
                        db.session.commit()
                        
                except Exception as e:
                    print(str(e))
                    return jsonify({
                        "code" : 500,
                        "error" : str(e),
                        "message": "Unable to commit to database."
                    }), 500
                        
                except Exception as e:
                    print(str(e))
                    return jsonify({
                        "code" : 500,
                        "error" : str(e),
                        "message": "Unable to commit to database."
                    }), 500
            for choice in quizChoice:
                localChoice = db.session.merge(choice)
                db.session.delete(localChoice)
                db.session.commit()
                
        except Exception as e:
            print(str(e))
            return jsonify({
                "code" : 500,
                "error" : str(e),
                "message": "Unable to commit to database."
            }), 500
        return jsonify({
                "code" : 201,
                "message": "Deletion Successful."
            }), 201

# Add new Quiz attempt
def addQuizAttempt(data):
    if not all(key in data.keys() for
                key in ('learnerId',"conductId", "sectionId", "attemptDate")):
                        return jsonify({
            "code" : 500,
            "message" : "Error, invalid input."
        }),500
    quizAttempt = LMSQuizAttempt()
    quizAttempt.learner_id = data["learnerId"]
    quizAttempt.conduct_id = data["conductId"]
    quizAttempt.section_id = data["sectionId"]
    quizAttempt.attempt_date = data["attemptDate"]
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

# Add new Quiz Performance
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

# Get all Quiz Question by section_id
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

# Get all Quiz Question and Quiz Choices by section_id
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

# Get all correct Quiz Choices for a Quiz by section_id
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

# Get Quiz Performance by quiz_attempt_id
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

# Update Quiz attempt with grade
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
        try:
            localQuiz = db.session.merge(quiz_attempt)
            localQuiz.grade = grade

            db.session.add(localQuiz)
            db.session.commit()

            return jsonify({
                "code" : 200,
                "data" : localQuiz.to_dict()
            }),200
        except Exception:
            return jsonify({
                "message": "Unable to commit to database."
            }), 500