from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import api.controllers.CourseController as courseController
import api.controllers.UserController as userController
import api.controllers.EnrolmentController as enrolmentController
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://" + "admin" + ":" + "#EW9%_ntPg8_-dt9" + "@" + "spm-bidding-cats.cbm12hznxdej.us-east-1.rds.amazonaws.com:3306" + "/" + "lms"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 100,
                                           'pool_recycle': 280}

db =SQLAlchemy(app)

CORS(app)


# USER ENDPOINTS

# Retrieve all users in the database
@app.route("/users")
def getAllUsers():
    return userController.getAllUsers()

# Retrieve a single user from the database
@app.route("/getasingleuser", methods=["POST"])
def getASingleUser():
    return userController.getASingleUser(request.get_json())

# Retrieve users by seniority level
@app.route("/usersbyseniority", methods=["POST"])
def getUsersBySeniority():
    return userController.getUsersBySeniority(request.get_json())

# Retreive user Id by email
@app.route("/retrieveuseridbyemail", methods=["POST"])
def retrieveUserIdByEmail():
    return userController.retrieveUserIdByEmail(request.get_json())

# Get all users that has completed a course by course id
@app.route("/getusersthathascompletedacourse", methods=["POST"])
def getUsersThatHasCompletedACourse():
    return userController.getUsersThatHasCompletedACourse(request.get_json())

# Get all engineers that are eligible for a course by course id
@app.route("/getallengineerseligibleforcoursebycourse", methods=["POST"])
def getEngineersThatAreEligibleForACourse():
    return userController.getEngineersThatAreEligibleForACourse(request.get_json())

# Get all engineers that are eligible for a course with pre-req by course id
@app.route("/getallengineerseligibleforcoursewithreqbycourse", methods=["POST"])
def getEngineersThatAreEligibleForACourseWithPreReq():
    return userController.getEngineersThatAreEligibleForACourseWithPreReq(request.get_json())

# Get all trainers that are eligible to teach a course by course_id
@app.route("/getalltrainerseligibletoteachacourse", methods=["POST"])
def getTrainersThatAreEligibleToTeachACourse():
    return userController.getTrainersThatAreEligibleToTeachACourse(request.get_json())


# Add a new user
@app.route("/adduser",methods=["POST"])
def addUser():
    return userController.addUser(request.get_json())



# COURSE ENDPOINTS

# Get all courses
@app.route("/getallcourses")
def getAllCourses():
    return courseController.getAllCourses()

# Get a single course
@app.route("/getasinglecourse", methods=["POST"])
def getASingleCourse():
    return courseController.getASingleCourse(request.get_json())

# Get all courses a user has enrolled
@app.route("/getallcoursesauserhasenrolled", methods=["POST"])
def getAllCoursesAUserHasEnrolled():
    return courseController.getAllCoursesAUserHasEnrolled(request.get_json())

# Get all completed courses that a user has by learner id
@app.route("/getallcompletedcoursesbyuserid", methods=["POST"])
def getAllCompletedCoursesByUserId():
    return courseController.getAllCompletedCoursesByUserId(request.get_json())

# Add a course
@app.route("/addacourse", methods=["POST"])
def addACourse():
    return courseController.addACourse(request.get_json())




# Enrolment Endpoints
@app.route("/getallselfenrolmentrequests")
def getAllSelfEnrolmentRequests():
    return enrolmentController.getallSelfEnrolmentRequest()


@app.route("/addnewenrolment", methods=["POST"])
def addNewEnrolment():
    return enrolmentController.addANewEnrolment(request.get_json())



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)