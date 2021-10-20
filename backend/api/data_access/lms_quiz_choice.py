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

    def getOptionID(self):
        return self.quiz_option_id
    
    def setOptionID(self,newID):
        self.quiz_option_id = newID

    def getQuestionID(self):
        return self.quiz_question_id

    def getOption(self):
        return self.option

    def setOption(self,new_option):
        if new_option!="" and len(new_option)<=45:
            self.option = new_option

    def getResult(self):
        return self.correct

    def setResult(self,new_result):
        if new_result in [0,1]:
            self.section_name = new_result
        else:
            raise Exception("A result can only be right or wrong")
    
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