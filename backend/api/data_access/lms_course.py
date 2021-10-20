from flask_sqlalchemy import SQLAlchemy
from app_config import app
from flask_cors import CORS
db = SQLAlchemy(app)
CORS(app)

class Course(db.Model):
    __tablename__ = "lms_course"
    course_id = db.Column(db.Integer, primary_key=True)
    course_requisite_id = db.Column(db.Integer)
    course_code = db.Column(db.VARCHAR(10))
    title = db.Column(db.VARCHAR(100))
    outline = db.Column(db.VARCHAR(500))
    badge = db.Column(db.VARCHAR(200))
    active = db.Column(db.SmallInteger(1))
    

    # Getter and setter methods

    def getCourseID(self):
        return self.course_id

    def getCourseCode(self):
        return self.course_code
    
    def setCourseCode(self,new_code):
        if new_code!="" and len(new_code)<=10:
            self.course_code = new_code

    def getTitle(self):
        return self.title
    
    def setTitle(self,new_title):
        if new_title!="" and len(new_title)<=50:
            self.title = new_title
    
    def getOutline(self):
        return self.outline
    
    def setOutline(self,new_outline):
        if new_outline!="" and len(new_outline)<=500:
            self.outline = new_outline

    def getCapcity(self):
        return self.capacity
    
    def setCapacity(self,new_capcity):
        self.capacity = new_capcity
    
    def incrementCapacity(self):
        self.capacity+=1

    def decrementCapacity(self):
        if self.capacity>0:
            self.capacity-=1
        else:
            raise Exception("Sorry, the course is full.")

    def getStartDate(self):
        return self.start_date
    
    
    
    # need research on how datetime is stored in python
    # need additional validators
    # 1. new_end not earlier than current date time
    # 2. new_end not earlier than start date
    def setEndDate(self,new_end):
        self.end_date = new_end

    
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