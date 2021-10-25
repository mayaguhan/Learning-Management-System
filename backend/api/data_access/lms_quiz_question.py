from flask_sqlalchemy import SQLAlchemy
from app_config import app
from flask_cors import CORS
db = SQLAlchemy(app)
CORS(app)

class QuizQuestion(db.Model):
    __tablename__ = "lms_quiz_question"
    quiz_question_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer,db.ForeignKey('lms_section.id'))#,primary_key=True)
    question_name = db.Column(db.VARCHAR(200))
    
    # as of 9 October, all methods are local and update operations have not been made yet
    # Getter and setter methods

    def getQuestionID(self):
        return self.quiz_question_id
    
    def setQuestionID(self,newID):
        self.quiz_question_id = newID

    def getSectionID(self):
        return self.section_id

    def getQuestionName(self):
        return self.question_name

    def setQuestionName(self,new_name):
        if new_name!="" and len(new_name)<=200:
            self.question_name = new_name
    
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