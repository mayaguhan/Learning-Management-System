from flask_sqlalchemy import SQLAlchemy
from ..data_access.lms_quiz_attempt import LMSQuizAttempt
from ..data_access.lms_quiz_question import LMSQuizQuestion
from ..data_access.lms_quiz_choice import LMSQuizChoice

db = SQLAlchemy()

class LMSQuizPerformance(db.Model):
    __tablename__ = "lms_quiz_performance"
    quiz_attempt_id = db.Column(db.Integer,db.ForeignKey(LMSQuizAttempt.quiz_attempt_id), primary_key=True)
    quiz_question_id = db.Column(db.Integer,db.ForeignKey(LMSQuizQuestion.quiz_question_id),primary_key=True)
    quiz_choice_id = db.Column(db.Integer,db.ForeignKey(LMSQuizChoice.quiz_choice_id),primary_key=True)
    
    # as of 9 October, all methods are local and update operations have not been made yet
    # Getter and setter methods
    def getAttemptID(self):
        return self.quiz_attempt_id

    def setAttemptID(self,newID):
        self.quiz_attempt_id = newID

    def getQuestionID(self):
        return self.quiz_question_id

    def setQuestionID(self,newID):
        self.quiz_question_id = newID

    def getChoiceID(self):
        return self.quiz_choice_id
    
    def setOptionID(self,newID):
        self.quiz_choice_id = newID

    
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