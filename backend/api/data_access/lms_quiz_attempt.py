# from backend.api.data_access.classes import LMSConduct
from flask_sqlalchemy import SQLAlchemy
from ..data_access.lms_user import LMSUser
from ..data_access.lms_section import LMSSection
from ..data_access.lms_section import LMSConduct
import datetime
from datetime import datetime

db = SQLAlchemy()

class LMSQuizAttempt(db.Model):
    __tablename__ = "lms_quiz_attempt"
    quiz_attempt_id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer,db.ForeignKey(LMSUser.user_id))
    section_id = db.Column(db.Integer,db.ForeignKey(LMSSection.section_id))
    conduct_id = db.Column(db.Integer,db.ForeignKey(LMSConduct.conduct_id))
    attempt_date = db.Column(db.DateTime)
    grade = db.Column(db.Integer)
    


    # Getter and setter methods

    def getAttemptID(self):
        return self.quiz_attempt_id

    def getSectionID(self):
        return self.section_id

    def setSectionID(self, newSection):
        if type(newSection)!=int:
            raise Exception("Invalid input")
        elif newSection<=0:
            raise Exception("DB auto id should never be negative")
        else:
            self.section_id = newSection
            return self.section_id
    
    def getLearnerID(self):
        return self.learner_id
    
    def setLearnerID(self, newLearner):
        if type(newLearner)!=int:
            raise Exception("Invalid input")
        elif newLearner<=0:
            raise Exception("DB auto id should never be negative")
        else:
            self.learner_id = newLearner
            return self.learner_id
        
    def getConductID(self):
        return self.conduct_id
    
    def setConductID(self, newConduct):
        if type(newConduct)!=int:
            raise Exception("Invalid input")
        elif newConduct<=0:
            raise Exception("DB auto id should never be negative")
        else:
            self.learner_id = newConduct
            return self.conduct_id

    def getAttemptDate(self):
        return self.attempt_date
    
    def setAttemptDate(self,newAttempt):
        if type(newAttempt)!=datetime:
            raise Exception("Invalid input")
        elif newAttempt>datetime.now():
            raise Exception("Can't set a date later than the current date time")
        else:
            self.attempt_date = newAttempt
            return self.attempt_date
    
    def getGrade(self):
        return self.grade
    
    def setGrade(self,newGrade):
        if type(newGrade)!=int:
            raise Exception("Invalid input")
        elif newGrade<0:
            raise Exception("Grade can't be negative")
        else:
            self.grade = newGrade
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