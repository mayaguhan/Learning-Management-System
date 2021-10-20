from flask_marshmallow import Schema
from marshmallow.fields import Str
from marshmallow.fields import Int

class UserSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["user_id", "username", "name", "email", "seniority_level", "contact"]

    
    user_id = Int()
    username = Str()
    name = Str()
    email = Str()
    seniority_level = Str()
    contact = Str()


class SeniorEngineerSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ["user_id", "username", "name", "email", "seniority_level", "contact", "salary"]

    
    user_id = Int()
    username = Str()
    name = Str()
    email = Str()
    seniority_level = Str()
    contact = Str()
    salary = Int()