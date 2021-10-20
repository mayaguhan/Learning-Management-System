from flask_sqlalchemy import SQLAlchemy
from app_config import app
from flask_cors import CORS
db = SQLAlchemy(app)
CORS(app)

class QuizPerformance(db.Model):
    __tablename__ = "lms_quiz_performance"
    quiz_attempt_id = db.Column(db.Integer,db.ForeignKey('lms_quiz_attempt.id'), primary_key=True)
    quiz_question_id = db.Column(db.Integer,db.ForeignKey('lms_quiz_question.id'),primary_key=True)
    quiz_option_id = db.Column(db.Integer,db.ForeignKey('lms_quiz_option.id'),primary_key=True)
    
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

    def getOptionID(self):
        return self.quiz_option_id
    
    def setOptionID(self,newID):
        self.quiz_option_id = newID

    
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