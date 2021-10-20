from flask_sqlalchemy import SQLAlchemy
from app_config import app
from flask_cors import CORS
db = SQLAlchemy(app)
CORS(app)

class Section(db.Model):
    __tablename__ = "lms_section"
    section_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer,db.ForeignKey('lms_course.id'))#, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('lms_user.id'))#,primary_key=True)
    section_name = db.Column(db.VARCHAR(50))
    quiz_duration = db.Column(db.Integer)
    passing_grade = db.Column(db.Integer)
    

    # Getter and setter methods

    def getSectionID(self):
        return self.section_id

    def getCourseID(self):
        return self.course_id

    def getTrainerID(self):
        return self.trainer_id

    def getSectionName(self):
        return self.section_name
    
    def setSectionName(self,new_name):
        if new_name!="" and len(new_name)<=50:
            self.section_name = new_name

    def getQuizDuration(self):
        return self.quiz_duration
    
    def setQuizDuration(self,new_duration):
        if new_duration>0:
            self.quiz_duration = new_duration
        else:
            raise Exception("Please give some time to your students.")

    def getPassingGrade(self):
        return self.passing_grade
    
    def setPassingGrade(self,new_grade):
        if new_grade>0:
            self.passing_grade = new_grade
        else:
            raise Exception("The passing grade has to be greater than 0")

    
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