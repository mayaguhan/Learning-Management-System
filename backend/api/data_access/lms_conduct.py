from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from lms_course import LMSCourse
from lms_user import LMSUser

db = SQLAlchemy()

class LMSConduct(db.Model):
    __tablename__ = "lms_conduct"
    conduct_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer,db.ForeignKey(LMSCourse.course_id))
    trainer_id = db.Column(db.Integer,db.ForeignKey(LMSUser.user_id))
    capacity = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    start_register = db.Column(db.DateTime)
    end_register = db.Column(db.DateTime)
    
    def getCapacity(self):
        return self.capacity

    def setCapacity(self,new_capacity):
        if new_capacity>0:
            self.capacity = new_capacity
        else:
            raise Exception("Please set a capcacity greater than 0.")
    
    def incrementCapacity(self):
        self.capacity+=1

    def decrementCapacity(self):
        if self.capacity>0:
            self.capacity-=1
        else:
            raise Exception("Sorry, the course is full.")
    
    def getStartDate(self):
        return self.start_date
    
    def setStartDate(self,newStartDate):
        if newStartDate<datetime.now():
            raise Exception("The course is already ongoing.")
        elif newStartDate>self.end_date:
            raise Exception("The course cannot start after it is scheduled to end!")
        else:
            self.start_date=newStartDate

    def getEndDate(self):
        return self.end_date
    
    def setEndDate(self,newEndDate):
        if newEndDate<datetime.now():
            raise Exception("You can't set an end date earlier than today.")
        elif newEndDate<self.start_date:
            raise Exception("The course cannot end before it is scheduled to start!")
        else:
            self.end_date=newEndDate
    
    def getStartRegister(self):
        return self.start_register
    
    def setStartRegister(self,newStartRegister):
        if newStartRegister<datetime.now():
            raise Exception("You can't set a date before today")
        elif newStartRegister>self.end_register:
            raise Exception("Sign ups cannot start after it is scheduled to end!")
        else:
            self.start_register=newStartRegister
    
    def getEndRegister(self):
        return self.end_register
    
    def setEndRegister(self,newEndRegister):
        if newEndRegister<datetime.now():
            raise Exception("You cannot abruptly alter the end date to before today.")
        elif newEndRegister<self.start_register:
            raise Exception("Sign ups cannot end before it is scheduled to start!")
        else:
            self.end_register=newEndRegister
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