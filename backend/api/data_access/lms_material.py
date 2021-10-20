from flask_sqlalchemy import SQLAlchemy
from app_config import app
from flask_cors import CORS
db = SQLAlchemy(app)
CORS(app)

class Material(db.Model):
    __tablename__ = "lms_material"
    material_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer,db.ForeignKey('lms_section.id'))
    file_name = db.Column(db.VARCHAR(100))
    link = db.Column(db.VARCHAR(200))
    
    # as of 9 October, all methods are local and update operations have not been made yet
    # Getter and setter methods

    def getMaterialID(self):
        return self.material_id

    def getSectionID(self):
        return self.section_id

    def getMaterialName(self):
        return self.material_name

    def setMaterialName(self,new_name):
        if new_name!="" and len(new_name)<=100:
            self.material_name = new_name

    def getType(self):
        return self.type

    def setType(self,new_type):
        if new_type!="" and len(new_type)<=20:
            self.section_name = new_type

    def getLink(self):
        return self.link
    
    def setLink(self,new_link):
        if new_link!="" and len(new_link)<=200:
            self.link = new_link
    
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