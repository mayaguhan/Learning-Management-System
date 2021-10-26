from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LMSUser(db.Model):
    __tablename__ = "lms_user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(50))
    email = db.Column(db.VARCHAR(50))
    seniority_level = db.Column(db.VARCHAR(20))
    contact = db.Column(db.VARCHAR(20))

    # Getter and setter methods
    def getUserId(self):
        return self.user_id

    def getUsername(self):
        return self.username

    def setUsername(self,new_name):
        if new_name!="" and len(new_name)<=50:
            self.username = new_name

    def getName(self):
        return self.name

    def setName(self,new_name):
        if new_name!="" and len(new_name)<=50:
            self.name = new_name
    
    def getEmail(self):
        return self.email

    def setEmail(self,new_email):
        if new_email!="" and len(new_email)<=50:
            self.email = new_email

    def getSeniorityLevel(self):
        return self.seniority_level

    def setSeniorityLevel(self,new_seniority):
        if new_seniority!="" and len(new_seniority)<=20:
            self.seniority_level = new_seniority

    def getContact(self):
        return self.contact

    def setContact(self,new_contact):
        if new_contact!="" and len(new_contact)<=20:
            self.contact = new_contact
    
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