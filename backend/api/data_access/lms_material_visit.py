from flask_sqlalchemy import SQLAlchemy
from lms_material import LMSMaterial
from lms_user import LMSUser

db = SQLAlchemy()

class MaterialVisit(db.Model):
    __tablename__ = "lms_material_visit"
    material_id = db.Column(db.Integer,db.ForeignKey(LMSMaterial.material_id), primary_key=True)
    learner_id = db.Column(db.Integer,db.ForeignKey(LMSUser.user_id),primary_key=True)
    
    # Getter and setter methods
    def getMaterialID(self):
        return self.material_id
    
    def getLearnerID(self):
        return self.learner_id
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

