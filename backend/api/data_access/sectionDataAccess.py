from flask_sqlalchemy import SQLAlchemy
from userDataAccess import LMSUser
from courseDataAccess import courseData

db = SQLAlchemy()

class LMSConduct(LMSUser,courseData):
    __tablename__ = 'lms_course'
    trainerID = LMSUser.user_id