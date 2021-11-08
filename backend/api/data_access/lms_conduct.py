from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ..data_access.lms_course import LMSCourse
from ..data_access.lms_user import LMSUser

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

    def getConductId(self):
        return self.conduct_id
    
    def getCourseId(self):
        return self.course_id
    
    def getTrainerId(self):
        return self.trainer_id

    def getCapacity(self):
        return self.capacity

    def setCapacity(self,new_capacity):
        if type(new_capacity)!=int:
            raise Exception("Invalud data type")
        elif new_capacity>=0:
            self.capacity = new_capacity
            return self.capacity
        else:
            raise Exception("Please set a capcacity greater than 0.")
    
    def incrementCapacity(self):
        self.capacity+=1
        return self.capacity

    def decrementCapacity(self):
        if self.capacity>0:
            self.capacity-=1
            return self.capacity
        else:
            raise Exception("Sorry, the course is full.")
    
    def increaseCapacity(self, newSpaces):
        if type(newSpaces)!=int:
            raise Exception("Invalid data type")
        else:
            self.capacity+=newSpaces
            return self.capacity
    
    def decreaseCapacity(self, spacesTaken):
        if type(spacesTaken)!=int:
            raise Exception("Invalid input")
        elif (self.capacity-spacesTaken)<0:
            raise Exception("Number of slots exceeded")
        else:
            self.capacity-=spacesTaken
            return self.capacity
    def getStartDate(self):
        return self.start_date
    
    def setStartDate(self,newStartDate):
        if type(newStartDate)!=datetime:
            raise Exception("Invalid input")
        if newStartDate<datetime.now():
            raise Exception("The course is already ongoing.")
        elif newStartDate>self.end_date:
            raise Exception("The course cannot start after it is scheduled to end!")
        else:
            self.start_date=newStartDate
            return self.start_date

    def getEndDate(self):
        return self.end_date
    
    def setEndDate(self,newEndDate):
        if type(newEndDate)!=datetime:
            raise Exception("Invalid input")
        elif newEndDate<datetime.now():
            raise Exception("You can't set an end date earlier than today.")
        elif newEndDate<self.start_date:
            raise Exception("The course cannot end before it is scheduled to start!")
        else:
            self.end_date=newEndDate
            return self.end_date
    
    def getStartRegister(self):
        return self.start_register
    
    def setStartRegister(self,newStartRegister):
        if type(newStartRegister)!=datetime:
            raise Exception("Invalid input")
        elif newStartRegister<datetime.now():
            raise Exception("You can't set a date before today")
        elif newStartRegister>self.end_register:
            raise Exception("Sign ups cannot start after it is scheduled to end!")
        else:
            self.start_register=newStartRegister
            return self.start_register
    
    def getEndRegister(self):
        return self.end_register
    
    def setEndRegister(self,newEndRegister):
        if type(newEndRegister)!=datetime:
            raise Exception("Invalid input")
        elif newEndRegister<datetime.now():
            raise Exception("You cannot abruptly alter the end date to before today.")
        elif newEndRegister<self.start_register:
            raise Exception("Sign ups cannot end before it is scheduled to start!")
        else:
            self.end_register=newEndRegister
            return self.end_register
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