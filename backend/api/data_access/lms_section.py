from flask_sqlalchemy import SQLAlchemy
from ..data_access.lms_conduct import LMSConduct

db = SQLAlchemy()

class LMSSection(db.Model):
    __tablename__ = "lms_section"
    section_id = db.Column(db.Integer, primary_key=True)
    conduct_id = db.Column(db.Integer,db.ForeignKey(LMSConduct.conduct_id))#, primary_key=True)
    sequence = db.Column(db.Integer)
    section_name = db.Column(db.VARCHAR(50))
    quiz_duration = db.Column(db.Integer)
    passing_grade = db.Column(db.Integer)
    

    # Getter and setter methods

    def getSectionID(self):
        return self.section_id

    def getConductID(self):
        return self.conduct_id

    def getSequence(self):
        return self.sequence
    

    def getSectionName(self):
        return self.section_name
    
    def setSectionName(self,new_name):
        if type(new_name)!= str:
            raise Exception("Invalid input")
        elif new_name=="" or len(new_name)>50:
            raise Exception("Please give a name to this section")
        else:
            self.section_name = new_name
            return self.section_name
            

    def getQuizDuration(self):
        return self.quiz_duration
    
    def setQuizDuration(self,new_duration):
        if type(new_duration) != int:
            raise Exception("Invalid input")
        elif new_duration<0:
            raise Exception("Please give some time to your students.")
        else:
            self.quiz_duration = new_duration
            return self.quiz_duration

    def getPassingGrade(self):
        return self.passing_grade
    
    def setPassingGrade(self,new_grade):
        if type(new_grade)!=int:
            raise Exception("Invalid input")
        if new_grade<=0:
            raise Exception("The passing grade has to be greater than 0")
        else:
            self.passing_grade = new_grade
            return self.passing_grade

    
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