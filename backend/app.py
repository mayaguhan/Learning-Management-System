from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import api.controllers.CourseController as courseController
import api.controllers.UserController as userController
import api.controllers.EnrolmentController as enrolmentController
import api.controllers.QuizController as quizController
import api.controllers.SectionController as sectionController
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + "admin" + ":" + "#EW9%_ntPg8_-dt9" + "@" + "spm-bidding-cats.cbm12hznxdej.us-east-1.rds.amazonaws.com:3306" + "/" + "lms"  # noqa: E402, F401, E501
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db = SQLAlchemy(app)

CORS(app)


# USER ENDPOINTS

# Login User by email
@app.route("/retrieveuseridbyemail", methods=["POST"])
def retrieveUserIdByEmail():
    return userController.retrieveUserIdByEmail(request.get_json())


# Get all Users
@app.route("/users")
def getAllUsers():
    return userController.getAllUsers()


# Get a single User
@app.route("/getasingleuser", methods=["POST"])
def getASingleUser():
    return userController.getASingleUser(request.get_json())


# Get all Users by seniority_level
@app.route("/usersbyseniority", methods=["POST"])
def getUsersBySeniority():
    return userController.getUsersBySeniority(request.get_json())


# Get all Users that has completed a Course by course_id
@app.route("/getusersthathascompletedacourse", methods=["POST"])
def getUsersThatHasCompletedACourse():
    return userController.getUsersThatHasCompletedACourse(request.get_json())


# Get all Engineers that are eligible for a course by course id
@app.route("/getallengineerseligibleforcoursebycourse", methods=["POST"])
def getEngineersThatAreEligibleForACourse():
    return userController.getEngineersThatAreEligibleForACourse(request.get_json())  # noqa: E402, F401, E501


# Get all Engineers that are eligible for a course with requisite by course id
@app.route("/getallengineerseligibleforcoursewithreqbycourse", methods=["POST"])  # noqa: E402, F401, E501
def getEngineersThatAreEligibleForACourseWithPreReq():
    return userController.getEngineersThatAreEligibleForACourseWithPreReq(request.get_json())  # noqa: E402, F401, E501


# Get all Trainers eligible to teach a Course by course_id
@app.route("/getalltrainerseligibletoteachacourse", methods=["POST"])
def getTrainersThatAreEligibleToTeachACourse():
    return userController.getTrainersThatAreEligibleToTeachACourse(request.get_json())  # noqa: E402, F401, E501


# Get all Trainers that are conducting a Course by course_id
@app.route("/gettrainersconductingacourse", methods=["POST"])
def getTrainersConductingACourse():
    return userController.getTrainersConductingACourse(request.get_json())


# Get all Learners that are enrolled into a course by conduct_id
@app.route("/getlearnersenrolledbyconduct", methods=["POST"])
def getLearnersEnrolledByConduct():
    return userController.getLearnersEnrolledByConduct(request.get_json())


# Get quiz attempt for a section
@app.route("/getquizattemptforsection", methods=["POST"])
def getquizattemptforsection():
    return quizController.getQuizAttemptForSection(request.get_json())


# Get student quiz attempt by section id
@app.route("/getstudentquizattemptbysectionid", methods=["POST"])
def getstudentquizattemptbysectionid():
    return quizController.getStudentQuizAttemptBySectionId(request.get_json())


# Get quiz attempt by section id
@app.route("/getquizattemptpassingratebysectionid", methods=["POST"])
def getquizattemptpassingratebysectionid():
    return quizController.getQuizAttemptPassingRateBySectionId(request.get_json())  # noqa: E402, F401, E501


# Get quiz performance by section id
@app.route("/getquizquestionperformancebysectionid", methods=["POST"])
def getquizquestionperformancebysectionid():
    return quizController.getQuizQuestionPerformanceBySectionId(request.get_json())  # noqa: E402, F401, E501


# Get quiz performance by attempt and section id
@app.route("/getquizperformancebyattemptandsectionid", methods=["POST"])
def getquizperformancebyattemptandsectionid():
    return quizController.getQuizPerformanceByQuizAtemptAndSectionId(request.get_json())  # noqa: E402, F401, E501


# Delete quiz question by quiz question id
@app.route("/deletequizquestionbyid", methods=["DELETE"])
def deletequizquestionbyid():
    return quizController.deleteQuizQuestionByID(request.get_json())


# Delete quiz choice by quiz choice id
@app.route("/deletequizchoicebyid", methods=["DELETE"])
def deletequizchoicebyid():
    return quizController.deleteQuizChoiceByID(request.get_json())


# Add a new user
@app.route("/adduser", methods=["POST"])
def addUser():
    return userController.addUser(request.get_json())


# Get quiz performance by quiz attempt id
@app.route("/getquizperformancebyattemptid", methods=["POST"])
def getQuizPerformanceByAttemptId():
    return quizController.getQuizPerformanceByQuizAttemptID(request.get_json())


# Get quiz questions by section id
@app.route("/addquizattempt", methods=["POST"])
def addQuizAttempt():
    return quizController.addQuizAttempt(request.get_json())


# Get quiz questions by section id
@app.route("/getallcorrectquizchoicesbysectionid", methods=["POST"])
def getAllCorrectQuizChoicesBySectionId():
    return quizController.getAllCorrectQuizChoicesBySectionId(request.get_json())  # noqa: E402, F401, E501


# Get quiz questions by section id
@app.route("/getquizquestionsandchoicesbysectionid", methods=["POST"])
def getQuizQuestionsAndChoicesBySectionId():
    return quizController.getQuizQuestionsAndChoicesBySectionId(request.get_json())  # noqa: E402, F401, E501


# Get quiz questions by section id
@app.route("/getquizquestionsbysectionid", methods=["POST"])
def getQuizQuestionsBySectionId():
    return quizController.getQuizQuestionsBySectionId(request.get_json())


# Get material by section id
@app.route("/getmaterialsbysectionid", methods=["POST"])
def getMaterialBySectionId():
    return sectionController.getMaterialsBySectionID(request.get_json())


# Udpate quiz choice
@app.route("/updatequizchoice", methods=["POST"])
def updateQuizChoice():
    return quizController.updateQuizChoice(request.get_json())


# Update quiz question
@app.route("/updatequizquestion", methods=["POST"])
def updateQuizQuestion():
    return quizController.updateQuizQuestion(request.get_json())


# Add quiz performance
@app.route("/addnewquizperformance", methods=["POST"])
def addQuizPerformance():
    return quizController.addQuizPerformance(request.get_json())


# Add quiz choice
@app.route("/addnewchoice", methods=["POST"])
def addChoice():
    return quizController.addQuizChoice(request.get_json())


# Add quiz quesion
@app.route("/addquizquestion", methods=["POST"])
def addQuestion():
    return quizController.addQuizQuestion(request.get_json())


# Add new material visit
@app.route("/addnewmaterialvisit", methods=["POST"])
def addNewMaterialVisit():
    return sectionController.addNewMaterialVisit(request.get_json())


# Add new material
@app.route("/addnewmaterial", methods=["POST"])
def addNewMaterial():
    return sectionController.addNewMaterial(request.get_json())


# Delete material by ID
@app.route("/deletematerialbyid", methods=["DELETE"])
def deleteMaterialById():
    return sectionController.deleteMaterialByMaterialID(request.get_json())


# Update section details
@app.route("/updatesection", methods=["POST"])
def updateSection():
    return sectionController.updateSectionBySectionID(request.get_json())


# Get all sections by conduct id and user id
@app.route("/getallsectionsbyconductanduserid", methods=["POST"])
def getallsectionsbyconductanduserid():
    return sectionController.getAllSectionsByConductAndUserId(request.get_json())  # noqa: E402, F401, E501


# Delete section by ID
# @app.route("/deletesectionbyid",methods = ["DELETE"])
# def deleteSectionByID():
#     return sectionController.deleteSectionBySectionID(request.get_json())
# Update quiz attempt
@app.route("/getquizattempt", methods=["POST"])
def getQuizAttempt():
    return quizController.getQuizAttempyByID(request.get_json())


# Update quiz attempt
@app.route("/updatequizattempt", methods=["PUT"])
def updateAttempt():
    print(request)
    print(request.get_json())
    return quizController.updateQuizAttemptGrade(request.get_json())


# COURSE ENDPOINTS

# Get all courses
@app.route("/getallcourses")
def getAllCourses():
    return courseController.getAllCourses()


# Get a single course
@app.route("/getasinglecourse", methods=["POST"])
def getASingleCourse():
    return courseController.getASingleCourse(request.get_json())


# Get a Single Course Conducted information by conduct_id
@app.route("/getcourseconductinformation", methods=["POST"])
def getCourseConductInformation():
    return courseController.getCourseConductInformation(request.get_json())


# Get all Courses a User has Enrolled
@app.route("/getallcoursesauserhasenrolled", methods=["POST"])
def getAllCoursesAUserHasEnrolled():
    return courseController.getAllCoursesAUserHasEnrolled(request.get_json())


# Get all in-progress Courses a User has by learner_id
@app.route("/getallinprogresscoursesbyuserid", methods=["POST"])
def getAllInProgressCoursesByUserId():
    return courseController.getAllInProgressCoursesByUserId(request.get_json())


# Get all completed courses that a user has by learner id
@app.route("/getallcompletedcoursesbyuserid", methods=["POST"])
def getAllCompletedCoursesByUserId():
    return courseController.getAllCompletedCoursesByUserId(request.get_json())


# Get all Courses a User has not Enrolled In
@app.route("/getallcoursesauserhasnotenrolledin", methods=["POST"])
def getAllCoursesUserHasNotEnrolledIn():
    return courseController.getAllCoursesUserHasNotEnrolledIn(request.get_json())  # noqa: E402, F401, E501


# Get all Courses that are conducted by trainer_id
@app.route("/getallcoursesconductedbytrainer", methods=["POST"])
def getAllCoursesConductedByTrainer():
    return courseController.getAllCoursesConductedByTrainer(request.get_json())


# Add a course
@app.route("/addacourse", methods=["POST"])
def addACourse():
    return courseController.addACourse(request.get_json())


# Update Update Course by course_id
@app.route("/updateCourse", methods=["PUT"])
def updateCourse():
    return courseController.updateCourse(request.get_json())


# Add new Course Conduct
@app.route("/addcourseconduct", methods=["POST"])
def addCourseConduct():
    return courseController.addCourseConduct(request.get_json())


# Enrolment Endpoints

# Get all Self-Enrolment request (HR)
@app.route("/getallselfenrolmentrequests")
def getAllSelfEnrolmentRequests():
    return enrolmentController.getallSelfEnrolmentRequest()


# Get all Self-Enrolment request by learner_id
@app.route("/getlearnerselfenrolmentrequests", methods=["POST"])
def getLearnerSelfEnrolmentRequests():
    return enrolmentController.getLearnerSelfEnrolmentRequests(request.get_json())  # noqa: E402, F401, E501


# Add new Enrolment
@app.route("/addnewenrolment", methods=["POST"])
def addNewEnrolment():
    return enrolmentController.addANewEnrolment(request.get_json())


# Update Enrolment by learner_id and conduct_id
@app.route("/updateenrolment", methods=["PUT"])
def updateEnrolment():
    return enrolmentController.updateEnrolment(request.get_json())

# Update Enrolment by learner_id and conduct_id
@app.route("/updatecourseascomplete", methods=["PUT"])
def updateCourseAsComplete():
    return enrolmentController.updateCourseAsComplete(request.get_json())

# Delete an Enrolment request by learner_id and conduct_id
@app.route("/deleteenrolment", methods=["DELETE"])
def deleteEnrolment():
    return enrolmentController.deleteEnrolment(request.get_json())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
