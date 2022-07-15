import datetime
import base64
SECRET_KEY = 'some.secret.key'

def generate_token(user_id):
    payload = {'userId': user_id,
               'iat': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=60)}
    payload = str(payload)
    header = '{"alg":"HS256","typ":"JWT"}'
    signature = SECRET_KEY
    return f'{base64.b64encode(header)}.{base64.b64encode(payload)}.{base64.b64encode(signature)}'
