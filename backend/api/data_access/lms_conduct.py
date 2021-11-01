from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LMSConduct(db.Model):
    __tablename__ = "lms_conduct"
    conduct_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer,db.ForeignKey('lms_course.id'))
    trainer_id = db.Column(db.Integer,db.ForeignKey('lms_user.id'))
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
    
    def getStartDate(self):
        return self.start_date
    
    def getEndDate(self):
        return self.end_date
    
    def getStartRegister(self):
        return self.start_register
    
    def getEndRegister(self):
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