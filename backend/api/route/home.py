from api.schema.user import UserSchema
from api.schema.data import CourseDataSchema
from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from
from api.controllers import UserController, CourseController

home_api = Blueprint('api', __name__)


# USER ENDPOINTS

@home_api.route('/user')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Get all users',
            'schema': UserSchema
        }
    }
})

def user():
    return UserController.getAll()


@home_api.route('/userbytype', methods=['POST'])
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Get users by type',
            'schema': UserSchema
        }
    }
})

def userByType():

    userType = request.get_json()["type"]

    return UserController.getByType(userType)




# COURSE ENDPOINTS

@home_api.route('/courses')
@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Get all courses',
            'schema': CourseDataSchema
        }
    }
})

def course():
    return CourseController.getAll()

# courses that have pre req
# @home_api.route('/coursesWithPreReq')
# @swag_from({
#     'responses': {
#         HTTPStatus.OK.value: {
#             'description': 'Get all courses',
#             'schema': CourseDataSchema
#         }
#     }
# })

# def course():
#     return CourseController.getAll()