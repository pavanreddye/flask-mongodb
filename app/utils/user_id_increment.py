
from instance import mongo

def auto_increment_id(label):
    if label == "user":
        user_details = mongo.db.users
        count = user_details.find({}).count()
        count +=1
        return count

    elif label == "group":
        group_details = mongo.db.groups
        count = group_details.find({}).count()
        count += 1
        return count

