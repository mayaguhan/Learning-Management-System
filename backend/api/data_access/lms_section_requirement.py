from flask_sqlalchemy import SQLAlchemy
from lms_section import LMSSection

db = SQLAlchemy()

class LMSSectionRequirement(db.Model):
    __tablename__ = "lms_section_requirement"
    section_id = db.Column(db.Integer,db.ForeignKey(LMSSection.section_id), primary_key=True)
    section_requisite_id = db.Column(db.Integer,db.ForeignKey(LMSSection.section_id), primary_key=True)
    
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