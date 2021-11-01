from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
        if new_name!="" and len(new_name)<=50:
            self.name = new_name
        else:
            raise Exception("Please input a valid name")
    
    def getEmail(self):
        return self.email

    def setEmail(self,new_email):
        if new_email!="" and len(new_email)<=50:
            self.email = new_email
        else:
            raise Exception("Please input a valid email")

    def getSeniorityLevel(self):
        return self.seniority_level

    def setSeniorityLevel(self,new_seniority):
        if new_seniority!="" and len(new_seniority)<=20:
            self.seniority_level = new_seniority
        else:
            raise Exception("Please input a valid seniority level")

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

class LMSCourse(db.Model):
    __tablename__ = "lms_course"
    course_id = db.Column(db.Integer, primary_key=True)
    course_requisite_id = db.Column(db.Integer)
    course_code = db.Column(db.VARCHAR(10))
    title = db.Column(db.VARCHAR(100))
    outline = db.Column(db.VARCHAR(500))
    badge = db.Column(db.VARCHAR(200))
    active = db.Column(db.SmallInteger())
    

    # Getter and setter methods

    def getCourseID(self):
        return self.course_id
    
    def getCourseRequisiteID(self):
        return self.course_requisite_id

    def getCourseCode(self):
        return self.course_code
    
    def setCourseCode(self,new_code):
        if new_code!="" and len(new_code)<=10:
            self.course_code = new_code
        else:
            raise Exception("Invalid input")

    def getTitle(self):
        return self.title
    
    def setTitle(self,new_title):
        if new_title!="" and len(new_title)<=50:
            self.title = new_title
        else:
            raise Exception("Invalid input")
    
    def getOutline(self):
        return self.outline
    
    def setOutline(self,new_outline):
        if new_outline!="" and len(new_outline)<=500:
            self.outline = new_outline
        else:
            raise Exception("Invalid input")

    def getBadge(self):
        return self.badge
    
    def setBadge(self,new_badge):
        if new_badge!="" and len(new_badge)<=200:
            self.badge = new_badge
        else:
            raise Exception("Invalid input")

    def getActive(self):
        return self.active
    
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

class LMSConduct(db.Model):
    __tablename__ = "lms_conduct"
    conduct_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer,db.ForeignKey(LMSCourse.course_id))
    trainer_id = db.Column(db.Integer,db.ForeignKey(LMSUser.user_id))
    capacity = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    start_register = db.Column(db.DateTime)
    end_register = db.Column(db.DateTime)
    
    def getCapacity(self):
        return self.capacity

    def setCapacity(self,new_capacity):
        if new_capacity>0:
            self.capacity = new_capacity
        else:
            raise Exception("Please set a capcacity greater than 0.")
    
    def incrementCapacity(self):
        self.capacity+=1

    def decrementCapacity(self):
        if self.capacity>0:
            self.capacity-=1
        else:
            raise Exception("Sorry, the course is full.")
    
    def getStartDate(self):
        return self.start_date
    
    def setStartDate(self,newStartDate):
        if newStartDate<datetime.now():
            raise Exception("The course is already ongoing.")
        elif newStartDate>self.end_date:
            raise Exception("The course cannot start after it is scheduled to end!")
        else:
            self.start_date=newStartDate

    def getEndDate(self):
        return self.end_date
    
    def setEndDate(self,newEndDate):
        if newEndDate<datetime.now():
            raise Exception("You can't set an end date earlier than today.")
        elif newEndDate<self.start_date:
            raise Exception("The course cannot end before it is scheduled to start!")
        else:
            self.end_date=newEndDate
    
    def getStartRegister(self):
        return self.start_register
    
    def setStartRegister(self,newStartRegister):
        if newStartRegister<datetime.now():
            raise Exception("You can't set a date before today")
        elif newStartRegister>self.end_register:
            raise Exception("Sign ups cannot start after it is scheduled to end!")
        else:
            self.start_register=newStartRegister
    
    def getEndRegister(self):
        return self.end_register
    
    def setEndRegister(self,newEndRegister):
        if newEndRegister<datetime.now():
            raise Exception("You cannot abruptly alter the end date to before today.")
        elif newEndRegister<self.start_register:
            raise Exception("Sign ups cannot end before it is scheduled to start!")
        else:
            self.end_register=newEndRegister
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
class LMSSection(db.Model):
    __tablename__ = "lms_section"
    section_id = db.Column(db.Integer, primary_key=True)
    conduct_id = db.Column(db.Integer,db.ForeignKey(LMSConduct.conduct_id))#, primary_key=True)
    sequence = db.Column(db.Integer)
    section_name = db.Column(db.VARCHAR(50))
    quiz_duration = db.Column(db.Integer)
    passing_grade = db.Column(db.Integer)
    

    # Getter and setter methods

    def getSectionID(self):
        return self.section_id

    def getConductID(self):
        return self.conduct_id

    def getSequence(self):
        return self.sequence
    

    def getSectionName(self):
        return self.section_name
    
    def setSectionName(self,new_name):
        if new_name!="" and len(new_name)<=50:
            self.section_name = new_name
        else:
            raise Exception("Please give a name to this section")

    def getQuizDuration(self):
        return self.quiz_duration
    
    def setQuizDuration(self,new_duration):
        if new_duration>0:
            self.quiz_duration = new_duration
        else:
            raise Exception("Please give some time to your students.")

    def getPassingGrade(self):
        return self.passing_grade
    
    def setPassingGrade(self,new_grade):
        if new_grade>0:
            self.passing_grade = new_grade
        else:
            raise Exception("The passing grade has to be greater than 0")

    
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

class LMSMaterial(db.Model):
    __tablename__ = "lms_material"
    material_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer,db.ForeignKey(LMSSection.section_id))
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
    
class MaterialVisit(db.Model):
    __tablename__ = "lms_material_visit"
    material_id = db.Column(db.Integer,db.ForeignKey(LMSMaterial.material_id), primary_key=True)
    conduct_id = db.Column(db.Integer,db.ForeignKey(LMSConduct.conduct_id), primary_key = True)
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



class LMSQuizAttempt(db.Model):
    __tablename__ = "lms_quiz_attempt"
    quiz_attempt_id = db.Column(db.Integer, primary_key=True)
    learner_id = db.Column(db.Integer,db.ForeignKey(LMSUser.user_id))
    section_id = db.Column(db.Integer,db.ForeignKey(LMSSection.section_id))
    attempt_date = db.Column(db.DateTime)
    grade = db.Column(db.Integer)
    

    # Getter and setter methods

    def getAttemptID(self):
        return self.quiz_attempt_id
    
    def setAttemptID(self,newAttempt):
        self.quiz_attempt_id = newAttempt

    def getSectionID(self):
        return self.section_id
    
    def getLearnerID(self):
        return self.learner_id

    def getAttemptDate(self):
        return self.attempt_date
    
    def getGrade(self):
        return self.grade
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
        
class LMSQuizQuestion(db.Model):
    __tablename__ = "lms_quiz_question"
    quiz_question_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer,db.ForeignKey(LMSSection.section_id))#,primary_key=True)
    question_name = db.Column(db.VARCHAR(200))
    
    # as of 9 October, all methods are local and update operations have not been made yet
    # Getter and setter methods

    def getQuestionID(self):
        return self.quiz_question_id
    
    def setQuestionID(self,newID):
        self.quiz_question_id = newID

    def getSectionID(self):
        return self.section_id

    def getQuestionName(self):
        return self.question_name

    def setQuestionName(self,new_name):
        if new_name!="" and len(new_name)<=200:
            self.question_name = new_name
    
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

class LMSQuizChoice(db.Model):
    __tablename__ = "lms_quiz_choice"
    quiz_choice_id = db.Column(db.Integer, primary_key=True)
    quiz_question_id = db.Column(db.Integer,db.ForeignKey(LMSQuizQuestion.quiz_question_id))#,primary_key=True)
    choice = db.Column(db.VARCHAR(50))
    correct = db.Column(db.SmallInteger())
    
    # as of 9 October, all methods are local and update operations have not been made yet
    # Getter and setter methods

    def getChoiceID(self):
        return self.quiz_choice_id
    
    def setChoiceID(self,newID):
        self.quiz_choice_id = newID

    def getQuestionID(self):
        return self.quiz_question_id

    def getChoice(self):
        return self.choice

    def setChoice(self,newChoice):
        if len(newChoice)>50 or len(newChoice)==0:
            raise Exception("Choice invalid")
        else:
            self.choice = newChoice
    
    def getResult(self):
        return self.correct
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

class LMSQuizPerformance(db.Model):
    __tablename__ = "lms_quiz_performance"
    quiz_attempt_id = db.Column(db.Integer,db.ForeignKey(LMSQuizAttempt.quiz_attempt_id), primary_key=True)
    quiz_question_id = db.Column(db.Integer,db.ForeignKey(LMSQuizQuestion.quiz_question_id),primary_key=True)
    quiz_choice_id = db.Column(db.Integer,db.ForeignKey(LMSQuizChoice.quiz_choice_id),primary_key=True)
    
    # as of 9 October, all methods are local and update operations have not been made yet
    # Getter and setter methods
    def getAttemptID(self):
        return self.quiz_attempt_id

    def setAttemptID(self,newID):
        self.quiz_attempt_id = newID

    def getQuestionID(self):
        return self.quiz_question_id

    def setQuestionID(self,newID):
        self.quiz_question_id = newID

    def getChoiceID(self):
        return self.quiz_choice_id
    
    def setOptionID(self,newID):
        self.quiz_choice_id = newID

    
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


