from flask_sqlalchemy import SQLAlchemy
import re

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

    def getName(self):
        return self.name

    def setName(self,new_name):
        if type(new_name)!= str:
            raise Exception("Invalid input")
        elif new_name=="" or len(new_name)>50:
            raise Exception("Please input a valid name")
        else:
            self.name = new_name
            return self.name

    def getEmail(self):
        return self.email

    def setEmail(self,new_email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if type(new_email)!= str:
            raise Exception("Invalid input")
        elif new_email=="" or len(new_email)>50:
            raise Exception("Please input a valid email")
        elif not re.fullmatch(regex,new_email):
            raise Exception("Invalid email")
        else:
            self.email = new_email
            return self.email

    def getSeniorityLevel(self):
        return self.seniority_level

    def setSeniorityLevel(self,new_seniority):
        allowed = ["HR","Engineer", "Senior Engineer"]
        if type(new_seniority)!= str:
            raise Exception("Invalid input")
        elif new_seniority=="" or len(new_seniority)>20:
            raise Exception("Please input a valid seniority level")
        elif new_seniority not in allowed:
            raise Exception("No such seniority level. Check again.")
        else:
            self.seniority_level = new_seniority
            return self.seniority_level

    def getContact(self):
        return self.contact

    def setContact(self,new_contact):
        if type(new_contact)!= str:
            raise Exception("Invalid input")
        elif new_contact=="" or len(new_contact)>20:
            raise Exception("Invalid contact")
        else:
            self.contact = new_contact
            return self.contact
    
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