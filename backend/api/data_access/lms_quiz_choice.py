from flask_sqlalchemy import SQLAlchemy
from app_config import app
from flask_cors import CORS
db = SQLAlchemy(app)
CORS(app)

class QuizOption(db.Model):
    __tablename__ = "lms_quiz_option"
    quiz_choice_id = db.Column(db.Integer, primary_key=True)
    quiz_question_id = db.Column(db.Integer,db.ForeignKey('lms_quiz_question.id'))#,primary_key=True)
    choice = db.Column(db.VARCHAR(50))
    correct = db.Column(db.SmallInteger(1))
    
    # as of 9 October, all methods are local and update operations have not been made yet
    # Getter and setter methods

    def getChoiceID(self):
        return self.quiz_choice_id
    
    def setChoiceID(self,newID):
        self.quiz_choice_id = newID

    def getQuestionID(self):
        return self.quiz_question_id

    def getChoice(self):
        return self.choice

    def setChoice(self,newChoice):
        if len(newChoice)>50 or len(newChoice)==0:
            raise Exception("Choice invalid")
        else:
            self.choice = newChoice
    
    def getResult(self):
        return self.correct
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