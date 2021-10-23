from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class userData(db.Model):
    __tablename__ = 'lms_user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(50))
    name = db.Column(db.VARCHAR(50))
    email = db.Column(db.VARCHAR(50))
    seniority_level = db.Column(db.VARCHAR(20))
    contact = db.Column(db.VARCHAR(20))

class LMSUser(db.Model):
    __tablename__ = 'lms_user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(50))
    name = db.Column(db.VARCHAR(50))
    email = db.Column(db.VARCHAR(50))
    seniority_level = db.Column(db.VARCHAR(20))
    contact = db.Column(db.VARCHAR(20))

    __mapper_args__ = {
        'polymorphic_identity': 'LMSUser'
    }

    def to_dict(self):
        """
        converts DB LMSUser object to local LMSUser object
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

class SeniorEngineer(LMSUser):
    __tablename__ = 'senior_engineer'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Engineer(LMSUser):
    __tablename__ = 'engineer'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class Admin(LMSUser):
    __tablename__ = 'admin'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    