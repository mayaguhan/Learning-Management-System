from flask_sqlalchemy import SQLAlchemy
from app_config import app
from flask_cors import CORS
db = SQLAlchemy(app)
CORS(app)

class Course(db.Model):
    __tablename__ = "lms_quiz_attempt"
    quiz_attempt_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer,db.ForeignKey('lms_section.id'))
    learner_id = db.Column(db.Integer,db.ForeignKey('lms_user.id'))
    course_id = db.Column(db.Integer,db.ForeignKey('lms_course.id'))
    trainer_id = db.Column(db.Integer,db.ForeignKey('lms_user.id'))
    attempt_date = db.Column(db.DateTime)
    grade = db.Column(db.Integer)
    

    # Getter and setter methods

    def getAttemptID(self):
        return self.quiz_attempt_id
    
    def setAttemptID(self,newAttempt):
        self.quiz_attempt_id = newAttempt

    def getSectionID(self):
        return self.section_id
    
    def getLearnerID(self):
        return self.learner_id

    def getCourseID(self):
        return self.course_id

    def getTrainerID(self):
        return self.trainer_id

    def getAttemptDate(self):
        return self.attempt_date
    
    def getGrade(self):
        return self.grade
    # 2 way translation
    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result