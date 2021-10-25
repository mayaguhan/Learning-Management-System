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
    
    def getCourseRequisiteID(self):
        return self.course_requisite_id

    def getCourseCode(self):
        return self.course_code
    
    def setCourseCode(self,new_code):
        if new_code!="" and len(new_code)<=10:
            self.course_code = new_code
        else:
            raise Exception("Invalid input")

    def getTitle(self):
        return self.title
    
    def setTitle(self,new_title):
        if new_title!="" and len(new_title)<=50:
            self.title = new_title
        else:
            raise Exception("Invalid input")
    
    def getOutline(self):
        return self.outline
    
    def setOutline(self,new_outline):
        if new_outline!="" and len(new_outline)<=500:
            self.outline = new_outline
        else:
            raise Exception("Invalid input")

    def getBadge(self):
        return self.badge
    
    def setBadge(self,new_badge):
        if new_badge!="" and len(new_badge)<=200:
            self.badge = new_badge
        else:
            raise Exception("Invalid input")

    def getActive(self):
        return self.active
    
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