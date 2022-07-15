from flask import request
import json
import datetime
from bson import json_util
from instance import mongo
from app.utils.create_token import generate_token
from app.utils.password_hash import create_hash_password,encode_password
from app.utils.user_id_increment import auto_increment_id
import requests
import random
import string

base_url = 'http://127.0.0.1:9090'

def create_user():
    try:
        user_details = mongo.db.users
        data = request.json
        if data in [{}, None]:
            output = "Please enter the proper post body"
            status = 400
            return output, status
        name = data['name']
        password_string = ''.join([random.choice(string.ascii_letters + string.digits) for _ in xrange(10)])
        password = encode_password(password_string)
        data['password'] = password
        _id = auto_increment_id("user")
        if _id is None:
            _id = 1
        data['user_id'] = int(_id)
        integrity = user_details.find({"name": name}).count()
        if integrity == 0:
            # user_id = user_details.insert({'name': name, 'email': email, 'address':address, 'mobile_no':mobile_no,'company':company})
            user_id = user_details.insert(data)
            new_user = user_details.find_one({'_id': user_id})
            user_id = new_user['_id']
            token = generate_token(user_id)
            email_body = {'subject': 'Account creation for ' + str(data['name']), "target_user_name": data['name'],
                          "login_id": data['email_id'], "password": password, "target_email_id": str(data['email_id']), "email_cc": "pavane.py@gmail.com"}

            #email_api = requests.post(base_url + '/create/user/email_notification', json=email_body)
            #print email_api
            output = {'name': new_user['name'], 'user_id': new_user['user_id'], 'token': token,
                      'address': new_user['address'], 'email': new_user['email_id'],
                      'message': 'New user created Succsfully'}
            status = 201
        else:
            status = 409
            output = "Another record with the similar name exists, Please try again with another name."
    except Exception as e:
        output = "An unexpected error occured in our servers. Please try again"
        status = 500
    finally:
        return output, status


def remove_user(user_id):
    if user_id == 1:
        status_code = 403
        message = "This is not an permissible action"
        return message, status_code
    user_details = mongo.db.users
    user_details = user_details.remove({'user_id': str(user_id)})
    if user_details['n'] == 1:
        message = "User Successfully deleted"
        status_code = 200
    else:
        message = "User Not Found"
        status_code = 404
    return message, status_code


def get_all_user_details():
    user_details = mongo.db.users
    user_data = user_details.find({})
    user_data = [json.loads(json.dumps(item, default=json_util.default)) for item in user_data]
    status_code = 200
    if None in user_data:
        user_data = "User Not Found"
        status_code = 404
    return user_data, status_code


def get_specific_user_details(user_id):
    user_details = mongo.db.users
    user_data = user_details.find_one({'user_id': str(user_id)})
    user_data = [json.loads(json.dumps(user_data, default=json_util.default))]
    status = 200
    if None in user_data:
        user_data = "User Not Found"
        status = 404
    return user_data, status


def update_user_details(data, user_id):
    user_details = mongo.db.users
    data = json.loads(data)
    user_id = data['user_id']
    time = datetime.datetime.utcnow()
    data['update_time'] = time
    update_user = user_details.update({'user_id': user_id}, data, upsert=False)
    if update_user['updatedExisting'] == True:
        message = "Updated Successfully"
        status_code = 200
    else:
        message = "User Not Found"
        status_code = 404
    return message, status_code

