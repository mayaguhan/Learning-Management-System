from flask_sqlalchemy import SQLAlchemy
from ..data_access.lms_user import LMSUser
from ..data_access.lms_section import LMSSection

db = SQLAlchemy()

class LMSQuizAttempt(db.Model):
    __tablename__ = "lms_quiz_attempt"
    quiz_attempt_id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer,db.ForeignKey(LMSUser.user_id))
    section_id = db.Column(db.Integer,db.ForeignKey(LMSSection.section_id))
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