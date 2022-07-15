from flask import request
import json
import datetime
from bson import json_util, ObjectId
from instance import mongo
from app.utils.create_token import generate_token
from app.utils.password_hash import create_hash_password,encode_password
from app.utils.user_id_increment import auto_increment_id
import requests
import random
import string

base_url = 'http://127.0.0.1:9090'

def add_group(data):
    try:
        groups_details = mongo.db.groups
        data = json.loads(data)
        if data in [{}, None]:
            message = "Please enter the proper post body"
            status = 400
            return message, status
        _id = auto_increment_id("group")
        if _id is None:
            _id = 1
        data['group_id'] = int(_id)
        name = data['group_name']
        group_integrity = groups_details.find({"name": name}).count()
        if group_integrity == 0:
            group_id = groups_details.insert(data)
            new_group = groups_details.find_one({'_id': group_id})
            message = {"group_id": new_group['group_id'],
                       'message': 'New Group created Succsfully'}
            status = 201
        else:
            status = 409
            message = "Another group name exists, Please try again with another name."

    except Exception as e:
        message = "An unexpected error occured in our servers. Please try again"
        status = 500
    finally:
        return message, status


def add_user_to_group(data,group_id):
    try:
        group_by_users = mongo.db.group_by_users
        data = json.loads(data)
        groups = mongo.db.groups
        groups_details = groups.find_one({"group_id": group_id})
        if groups_details is None:
            message = "Group not found"
            status = 404
        else:
            get_user_details = requests.get(f'{base_url}/get/user/' + str(data['user_id']))
            if get_user_details.status_code == 404:
                message = get_user_details.json()['data']
                status = get_user_details.status_code
            else:
                data = {"group_id":groups_details['group_id'],'group_type':groups_details['group_type'],"user_id": get_user_details.json()['data'][0]['user_id'],"user_name": get_user_details.json()['data'][0]['name'], "email_id": get_user_details.json()['data'][0]['email_id'], "company": get_user_details.json()['data'][0]['company'], "address": get_user_details.json()['data'][0]['address']}
                group_user_integrity = group_by_users.find({'$and': [{'group_id': group_id},{'user_id': data["user_id"]}]}).count()
                if group_user_integrity == 0:
                    group_by_users.insert(data)
                    group_user_data = group_by_users.find_one({'group_id':group_id})
                    group_user_data["message"] = "Succsfully Created group by user"
                    group_user_data = [json.loads(json.dumps(group_user_data, default=json_util.default))]
                    message = group_user_data
                    status = 200
                else:
                    message = "Another record with the similar group user details, Please try again with another name."
                    status = 409
    except Exception as e:
        message = "An unexpected error occured in our servers. Please try again"
        status = 500
    finally:
        return message, status


def group_name_update(group_id):
    group_details = mongo.db.groups
    group_details.find_one({'group_id':group_id})
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





