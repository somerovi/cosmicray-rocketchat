import json

import cosmicray


api = cosmicray.Cosmicray('cosmicray/rocketchat')
# ~/.cosmicray/
api.config['AUTH_CREDS_FILENAME'] = cosmicray.util.cosmicray_home('.rocketchatcreds')
api.config['AUTH_TOKEN_FILENAME'] = cosmicray.util.cosmicray_home('.rocketchattoken')


def authenticator(request):
    # All requests must be authenticated except for login and info
    if not request.is_request_for(login, info):
        token = Token.authenticate()
        return request.set_headers(**{
            'X-Auth-Token': token.authToken,
            'X-User-Id': token.userId})
    return request


def validate_response(resp):
    if resp.get('status') != 'success':
        raise TypeError('Rocketchat error: {}'.format(resp))
    return resp


@api.route('/api/v1/info', ['GET'])
def info(request):
    return request.response.json()


@api.route('/api/v1/login', ['POST'])
def login(request):
    '''
    https://docs.rocket.chat/developer-guides/rest-api/authentication/login

    request:
    :param json: { "user": "USERNAME", "password": "PASSWORD" }

    response:
    { "status": "success", "data": { "authToken": "TOKEN", "userId": "USERID" } }
    '''
    return request.map_model(
        validate_response(request.response.json()).get('data'))


@api.route('/api/v1/logout', ['GET'])
def logout(request):
    '''
    https://docs.rocket.chat/developer-guides/rest-api/authentication/logout

    response:
    { "status": "success", "data": { "message": "You've been logged out!" } }
    '''
    Token.clear_from_storage()
    return request.map_model(validate_response(request.response.json()).get('data'))


@api.route('/api/v1/me', ['GET'])
def me(request):
    '''
    https://docs.rocket.chat/developer-guides/rest-api/authentication/me

    response:
    { "_id": "aobEdbYhXfu5hkeqG", "name": "Example User",
      "emails": [ { "address": "example@example.com", "verified": true } ],
      "status": "offline", "statusConnection": "offline", "username": "example",
      "utcOffset": 0, "active": true, "success": true
    }
    '''
    return request.map_model(request.response.json())


class Token(cosmicray.model.Model):
    __route__ = login
    __fields__ = [
        'authToken',
        'userId'
    ]

    def create_payload(self):
        fpath = api.config['AUTH_CREDS_FILENAME']
        creds = cosmicray.util.read_artifact_file(fpath)
        return {'data': creds}

    @classmethod
    def authenticate(cls):
        token = cls.read_from_storage()
        if not token:
            token = Token().create()
            token.write_to_storage()
        return token

    @classmethod
    def clear_from_storage(cls):
        fpath = api.config['AUTH_TOKEN_FILENAME']
        cosmicray.util.write_artifact_file(fpath, 'session-expired')

    @classmethod
    def read_from_storage(cls):
        try:
            fpath = api.config['AUTH_TOKEN_FILENAME']
            data = json.loads(
                cosmicray.util.read_artifact_file(fpath))
            return Token(**data)
        except:
            pass

    def write_to_storage(self):
        fpath = api.config['AUTH_TOKEN_FILENAME']
        cosmicray.util.write_artifact_file(fpath, json.dumps(self.dict))
