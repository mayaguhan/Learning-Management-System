from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    def getFileName(self):
        return self.file_name

    def setFileName(self,new_name):
        if new_name!="" and len(new_name)<=100:
            self.file_name = new_name
        else:
            raise Exception("Invalid File Name")

    def getLink(self):
        return self.link
    
    def setLink(self,new_link):
        if new_link!="" and len(new_link)<=200:
            self.link = new_link
        else:
            raise Exception("Invalid link")
    
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