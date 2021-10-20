from flask import Flask, request, jsonify
from ..data_access.app_config import app,db
from ..data_access.lms_user import LMSUser


@app.route("/users")
def getAllPeople():
    users = LMSUser.query.all()
    if users:
        return jsonify(
            {
                "data":[user.to_dict() for user in users]
            }
        ),200
    else:
        return jsonify(
            {
                "message":"Oops no one exists"
            }
        ),404

@app.route("/usersBySeniority")
def getPersonBySeniority():
    data = request.get_json()
    seniority_level = data.seniority_level
    users = LMSUser.query.filter_by(seniority_level=seniority_level)
    if users:
        return jsonify(
            {
                "data":[user.to_dict() for user in users]
            }
        ),200
    else:
        return jsonify(
            {
                "message":"Oops no one has that seniority level."
            }
        ),404

@app.route("/users",methods=["POST"])
def add_user():
    data = request.get_json()
    if not all(key in data.keys for key in ("user_id","username","name","email","seniority_level","contact")):
        return jsonify(
            {
                "message" : "Incorrect JSON object provided"
            }
        ),500
    user = LMSUser(**data)
    try:
        db.session.add(user)
        db.commit
    except Exception:
        return jsonify(
            {
                "message" : "Looks like there was an issue writing to the database. Try again later."
            }
        ),500
# def getAll():
#     """
#     Returns user related details
#     A more detailed description of the endpoint
#     ---
#     """
#     result = userData.query.all()

#     returnDict = {}
#     for i in range(0, len(result)):

#         # For Engineer object creation and Return

#         # Serialize data from database into JSON
#         userSerialized = UserDataSchema().dump(result[i])

#         # Create Senior Engineer Object
#         senior = SeniorEngineer(userSerialized)

#         # Serialize Senior Engineer Object
#         seniorSerialized = SeniorEngineerSchema().dump(senior)
        
#         returnDict[i] = seniorSerialized


#         # For User Object Creation and Return

#         # Serialize data from database into JSON
#         # userSerialized = UserDataSchema().dump(result[i])

#         # Create User Obj
#         # user = User(userSerialized)
        
#         # Serialize User Object
#         # userSerialized = UserSchema().dump(user)

#         # Add it to the dictionary
#         # returnDict[i] = userSerialized

#     returnDict = json.dumps(returnDict)


#     return returnDict, 200


# def getByType(userType):
#     """
#     Returns users of the chosen type
#     Returns the users that belong to the chosen type. Request to be sent as JSON through the POST method
#     ---
#     """

#     result = userData.query.filter_by(seniority_level = userType).all()

#     returnDict = {}
#     for i in range(0, len(result)):
#         # Serialize data from database into JSON
#         userSerialized = UserDataSchema().dump(result[i])

#         # Create User Obj
#         user = User(userSerialized)
        
#         # Serialize User Object
#         userSerialized = UserSchema().dump(user)

#         # Add it to the dictionary
#         returnDict[i] = userSerialized

        
#     returnDict = json.dumps(returnDict)


#     return returnDict, 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
