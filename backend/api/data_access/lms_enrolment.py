from flask_sqlalchemy import SQLAlchemy
from app_config import app
from flask_cors import CORS
db = SQLAlchemy(app)
CORS(app)

class LMSEnrolment(db.Model):
    __tablename__ = "lms_enrolment"
    learner_id = db.Column(db.Integer, db.ForeignKey('lms_user.id'),primary_key=True)
    course_id = db.Column(db.Integer,db.ForeignKey('lms_course.id'), primary_key=True)
    trainer_id = db.Column(db.Integer,db.ForeignKey('lms_user.id'), primary_key=True)
    status = db.Column(db.VARCHAR(10))
    

    # Getter and setter methods

    def getStatus(self):
        return self.status

    def setStatus(self,new_status):
        if new_status!="" and len(new_status)<=10:
            self.username = new_status
    
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