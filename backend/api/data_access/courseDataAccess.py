from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


class courseData(db.Model):
    __tablename__ = 'lms_course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.VARCHAR(10))
    title = db.Column(db.VARCHAR(50))
    outline = db.Column(db.VARCHAR(500))
    start_date = db.Column(db.DATETIME)
    end_date = db.Column(db.DATETIME)


class courseRequirement(db.Model):
    __tablename__ = 'lms_course_requirement'
    course_id = db.Column(db.Integer, primary_key=True)
    course_requisite_id = db.Column(db.Integer, primary_key=True)