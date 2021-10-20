from flask_marshmallow import Schema
from marshmallow.fields import Str
from marshmallow.fields import Int

class UserDataSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["user_id", "username", "name", "email", "seniority_level", "contact"]

    
    user_id = Int()
    username = Str()
    name = Str()
    email = Str()
    seniority_level = Str()
    contact = Str()


class CourseDataSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["course_id", "course_code", "title", "outline", "start_date", "end_date", "course_requisite_id"]

    
    user_id = Int()
    course_code = Str()
    title = Str()
    outline = Str()
    start_date = Str()
    end_date = Str()
    course_requisite_id = Str()
