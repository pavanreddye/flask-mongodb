from flask import jsonify,make_response
from flask import request
from app.api_functions import user_authentication,email_send,group_based
from instance import app


@app.route('/create/user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        message, status_code = user_authentication.create_user()
        return make_response(jsonify(data= message), status_code)

@app.route('/delete/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if request.method == 'DELETE':
        message, status_code = user_authentication.remove_user(user_id)
        return make_response(jsonify(data= message), status_code)


@app.route('/get/user/<int:user_id>', methods=['GET'])
def get_specific_user(user_id):
    if request.method == 'GET':
        message, status_code = user_authentication.get_specific_user_details(user_id)
        return make_response(jsonify(data= message), status_code)


@app.route('/get/all/users', methods=['GET'])
def get_users():
    if request.method == 'GET':
        message, status_code = user_authentication.get_all_user_details()
        return jsonify({'data': message}), status_code


@app.route('/update/user/details/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if request.method == 'PUT':
        data = request.data
        message, status_code = user_authentication.update_user_details(data, user_id)
        return make_response(jsonify(data= message), status_code)


@app.route('/create/user/email_notification' ,methods=['POST'])
def user_email_nofitication():
    data = request.data
    message, status_code = email_send.send_email_notification(data)
    return make_response(jsonify(data=message) ,status_code)


@app.route('/create/group' ,methods=['POST'])
def create_group():
    data = request.data
    message, status_code = group_based.add_group(data)
    return make_response(jsonify(data=message) ,status_code)

@app.route('/add/user/group/<int:group_id>' ,methods=['POST','PUT'])
def add_group_user(group_id):
    if request.method == 'POST':
        data = request.data
        message, status_code = group_based.add_user_to_group(data,group_id)
        return make_response(jsonify(data=message) ,status_code)
    elif request.method == 'PUT':
        message, status_code = group_based



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9090)
