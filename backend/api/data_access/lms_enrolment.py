from flask_sqlalchemy import SQLAlchemy
from lms_user import LMSUser
from lms_conduct import LMSConduct

db = SQLAlchemy()

class LMSEnrolment(db.Model):
    __tablename__ = "lms_enrolment"
    learner_id = db.Column(db.Integer, db.ForeignKey(LMSUser.user_id),primary_key=True)
    conduct_id = db.Column(db.Integer,db.ForeignKey(LMSConduct.conduct_id), primary_key=True)
    self_enrolment = db.Column(db.SmallInteger())
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