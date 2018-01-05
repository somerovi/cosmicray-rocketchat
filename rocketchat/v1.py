import json

import cosmicray


api = cosmicray.Cosmicray('rocketchat')
# ~/.cosmicray/rocketchat
api.config['AUTH_CREDS_FILENAME'] = api.home_dir('creds')
api.config['AUTH_TOKEN_FILENAME'] = api.home_dir('token')
api.config['RAISE_FOR_STATUS'] = False


ENTITY_BODY_MAP = {
    'channels': 'channel',
    'groups': 'group',
    'im': 'ims'
}

ENTITY_PLURAL_BODY_MAP = {
    'channels': 'channels',
    'groups': 'groups',
    'im': 'ims'
}

def authenticator(request):
    # All requests must be authenticated except for login and info
    if not request.is_request_for(login, info):
        token = Token.authenticate()
        return request.set_headers(**{
            'X-Auth-Token': token.authToken,
            'X-User-Id': token.userId})
    return request


def validate_response(response):
    try:
        jdata = response.json()
    except (ValueError, TypeError):
        raise RocketChatError('response is not JSON', 'json-error')
    success = (('success' in jdata and jdata['success']) or
               ('status' in jdata and jdata['status'] == 'success'))
    if not success:
        raise RocketChatError(
            jdata.get('error'), jdata.get('errorType'), response.status_code)
    return jdata


@api.route('/api/v1/info', ['GET'])
def info(response):
    '''Information about the Rocket.Chat server.'''
    return validate_response(response)


# https://docs.rocket.chat/developer-guides/rest-api/authentication


@api.route('/api/v1/login', ['POST'])
def login(response):
    '''Authenticate with the REST API.'''
    return validate_response(response).get('data')


@api.route('/api/v1/logout', ['GET'])
def logout(response):
    '''Invalidate your REST API authentication token.'''
    Token.clear_from_storage()
    return validate_response(response).get('data')


@api.route('/api/v1/me', ['GET'])
def me(response):
    '''Displays information about the authenticated user'''
    return validate_response(response)


# TODO:
# https://rocket.chat/docs/developer-guides/rest-api/livechat


@api.route('/api/v1/livechat/users/{type}/{_id}', ['GET', 'POST', 'DELETE'],
           urlargs=[cosmicray.Param('type', options=['agent', 'department'])])
def livechat_users(response):
    """ GET Get a list of agents or managers. """
    """ POST Create a new livechat agent or manager. """
    """ GET Retrieve agent or manager data. """
    """ DELETE Removes a livechat agent or manager. """
    return validate_response(response)


@api.route('/api/v1/livechat/department/{_id}', ['GET', 'POST', 'PUT', 'DELETE'])
def livechat_department(response):
    """ GET Get a list of livechat departments. info"""
    """ POST Creates a new livechat department. info"""
    """ GET Retrieve a livechat department data. info"""
    """ PUT Updates a livechat department data. info"""
    """ DELETE Delete a livechat department. info"""
    return validate_response(response)


@api.route('/api/v1/livechat/sms-incoming/{service}', ['POST'],
           urlargs=[cosmicray.Param('service', default='twillio', options=['twillio'])])
def livechat_sms_incoming(response):
    """ POST Send SMS messages to Rocket.Chat. info"""
    return validate_response(response)


# TODO:
# https://rocket.chat/docs/developer-guides/rest-api/integration


@api.route('/api/v1/integrations.create', ['POST'])
def integrations_create(response):
    """Creates an integration. Link"""
    return validate_response(response)


@api.route('/api/v1/integrations.list', ['POST'])
def integrations_list(response):
    """Lists all of the integrations. Link"""
    return validate_response(response)


@api.route('/api/v1/integrations.remove', ['POST'])
def integrations_remove(response):
    """Removes an integration. Link"""
    return validate_response(response)



"""
https://docs.rocket.chat/developer-guides/rest-api/chat/
"""


@api.route('/api/v1/chat.getMessage', ['POST'])
def message_get(response):
    '''Retrieves a single chat message.
    request:
    { "msgId": "7aDSXtjMA3KPLxLjt" }

    response:
    { "message": { "_id": "7aDSXtjMA3KPLxLjt", "rid": "GENERAL",
        "msg": "This is a test!", "ts": "2016-12-14T20:56:05.117Z",
        "u": { "_id": "y65tAmHs93aDChMWu", "username": "graywolf336" } },
      "success": true }
    '''
    return validate_response(response).get('message')


@api.route('/api/v1/chat.postMessage', ['POST'])
def message_post(response):
    '''Posts a new chat message.

    request:
    { "channel": "#general", "text": "This is a test!" }

    More examples:
    https://docs.rocket.chat/developer-guides/rest-api/chat/postmessage#message-object-example

     '''
    return validate_response(response).get('message')


@api.route('/api/v1/chat.update', ['POST'])
def message_update(response):
    '''Updates the text of the chat message.'''
    return validate_response(response).get('message')


@api.route('/api/v1/chat.delete', ['POST'])
def message_delete(response):
    '''Deletes an existing chat message.
    request
    { "roomId": "ByehQjC44FwMeiLbX", "msgId": "7aDSXtjMA3KPLxLjt", "asUser": true }

    response:
    { "_id": "7aDSXtjMA3KPLxLjt", "ts": 1481741940895, "success": true }
    '''
    return validate_response(response)



@api.route('/api/v1/chat.pinMessage', ['POST'])
def message_pin(response):
    '''Pins a chat message to the messages channel.
    request:
    { "messageId": "7aDSXtjMA3KPLxLjt" }

    response:
    { "message": { "t": "message_pinned", "rid": "GENERAL", "ts": "2017-09-27T20:39:57.921Z",
        "msg": "", "u": { "_id": "Z3cpiYN6CNK2oXWKv", "username": "graywolf336"},
        "groupable": false, "attachments": [ {
            "text": "Hello", "author_name": "graywolf336",
            "author_icon": "/avatar/graywolf336?_dc=0", "ts": "2017-09-27T19:36:01.683Z" } ],
        "_updatedAt": "2017-09-27T20:39:57.921Z", "_id": "hmzxXKSWmMkoQyiAd" },
      "success": true}
    '''
    return validate_response(response).get('message')


@api.route('/api/v1/chat.react', ['POST'])
def message_react(response):
    '''Sets/unsets the users reaction to an existing chat message.'''
    return validate_response(response)


@api.route('/api/v1/chat.starMessage', ['POST'])
def message_star(response):
    '''Stars a chat message for the authenticated user.'''
    return validate_response(response)


@api.route('/api/v1/chat.unPinMessage', ['POST'])
def message_unpin(response):
    '''Removes the pinned status of the provided chat message.'''
    return validate_response(response)


@api.route('/api/v1/chat.unStarMessage', ['POST'])
def message_unstar(response):
    '''Removes the star on the chat message for the authenticated user.'''
    return validate_response(response)


"""
https://docs.rocket.chat/developer-guides/rest-api/channels/
https://rocket.chat/docs/developer-guides/rest-api/im
https://rocket.chat/docs/developer-guides/rest-api/groups
"""


@api.route('/api/v1/im.messages.others', ['GET'], params=[
    cosmicray.Param('roomId')])
def channels_private_messages(response):
    """Retrieves the messages from any private channel in the server.
    NOTE: Must ``Enable Direct Message History Endpoint`` otherwise returns 400
    """
    return validate_response(response).get('messages')


@api.route('/api/v1/im.list.everyone', ['GET'])
def channels_private_rooms(response):
    """Lists all private channels in the server.
    NOTE: Requires the permission ``view-room-administration``.
    """
    return validate_response(response).get('ims')


@api.route('/api/v1/channels.cleanHistory', ['POST'])
def channels_remove_messages(response):
    ''' Cleans up a channels history, requires special permission.'''
    return validate_response(response)


@api.route('/api/v1/channels.list.joined', ['GET'])
def channels_list_joined(response):
    '''Gets only the channels the calling user has joined.
    https://rocket.chat/docs/developer-guides/rest-api/channels/list-joined/
    '''
    return validate_response(response).get('channels')


@api.route('/api/v1/channels.setJoinCode', ['POST'])
def channels_set_join_code(response):
    ''' Sets the channels code required to join it.'''
    return validate_response(response)


@api.route('/api/v1/{channel_type}.list', ['GET'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups', 'im'])])
def channels_list(context, response):
    '''Retrives all of the channels from the server.'''
    key = ENTITY_PLURAL_BODY_MAP.get(context.urlargs['channel_type'])
    return validate_response(response).get(key)


@api.route('/api/v1/{channel_type}.info', ['GET'], params=[
    # Required (if no roomName) The channels id
    cosmicray.Param('roomId'),
    # Required (if no roomId) The channels name
    cosmicray.Param('roomName')], urlargs=[
        cosmicray.Param('channel_type', options=['channels', 'groups'])])
def channels_info(context, response):
    ''' Gets a channels information.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return validate_response(response).get(key)


@api.route('/api/v1/{channel_type}.history', ['GET'],
           params=[
               # Required The channels id
               cosmicray.Param('roomId', required=True),
               # Optional Default: now The end of time range of messages to retrieve
               cosmicray.Param('latest'),
               # Optional Default: n/a The start of the time range of messages to retrieve
               cosmicray.Param('oldest'),
               # Optional Default: false Whether messages which land on latest and oldest should be included
               cosmicray.Param('inclusive'),
               # Optional Default: 20 The amount of messages to retrieve
               cosmicray.Param('count'),
               # Optional Default: false Whether the amount of unreads should be included.
               cosmicray.Param('unreads')
           ],
           urlargs=[
               cosmicray.Param(
                   'channel_type', options=['channels', 'im', 'groups'])
           ])
def channels_messages(context, response):
    """Retrieves the messages from a public, group, or direct channel."""
    jdata = validate_response(response)
    messages = jdata.get('messages')
    for message in messages:
        message['channel_type'] = context.urlargs['channel_type']
        message['unreadNotLoaded'] = jdata.get('unreadNotLoaded')
    return messages


@api.route('/api/v1/{channel_type}.open', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups', 'im'])
])
def channels_open(response):
    ''' Adds the channel back to the users list of channels.'''
    return validate_response(response)


@api.route('/api/v1/{channel_type}.close', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups', 'im'])
])
def channels_close(response):
    ''' Removes a channel from a users list of channels.'''
    return validate_response(response)


@api.route('/api/v1/{channel_type}.addAll', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_add_all(response):
    '''
    Adds all of the users on the server to a channel.
    request:
    { "roomId": "ByehQjC44FwMeiLbX", "activeUsersOnly": true|false }
    '''
    return validate_response(response).get('channel')


@api.route('/api/v1/{channel_type}.{action}Moderator', ['POST'], urlargs=[
    cosmicray.Param('action', options=['add', 'remove']),
    cosmicray.Param('channel_type', options=['channels', 'groups'])])
def channels_moderator(response):
    ''' Gives the role of moderator to a user in a channel.'''
    ''' Removes the role of moderator from a user in a channel.'''
    return validate_response(response)


@api.route('/api/v1/{channel_type}.{action}Owner', ['POST'], urlargs=[
    cosmicray.Param('action', options=['add', 'remove']),
    cosmicray.Param('channel_type', options=['channels', 'groups'])])
def channels_owner(response):
    '''Gives the role of owner to a user in a channel.'''
    '''Removes the role of owner from a user in a channel.'''
    return validate_response(response)


@api.route('/api/v1/{channel_type}.create', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_create(context, response):
    '''Creates a new channel.
    https://rocket.chat/docs/developer-guides/rest-api/channels/create/
    '''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return validate_response(response).get(key)


@api.route('/api/v1/{channel_type}.archive', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_archive(response):
    '''Archives a channel.
    https://rocket.chat/docs/developer-guides/rest-api/channels/archive/
    '''
    return validate_response(response)


@api.route('/api/v1/{channel_type}.unarchive', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_unarchive(response):
    '''Unarchives a channel.
    https://rocket.chat/docs/developer-guides/rest-api/channels/unarchive/
    '''
    return validate_response(response)

@api.route('/api/v1/{channel_type}.getIntegrations', ['GET'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_get_integrations(response):
    ''' Gets the channels integration.'''
    return validate_response(response)


@api.route('/api/v1/{channel_type}.invite', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_invite(context, response):
    '''Adds a user to a channel.
    https://rocket.chat/docs/developer-guides/rest-api/channels/invite/
    '''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return validate_response(response).get(key)


@api.route('/api/v1/{channel_type}.kick', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_kick(context, response):
    ''' Removes a user from a channel.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return validate_response(response).get(key)


@api.route('/api/v1/{channel_type}.leave', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_leave(context, response):
    ''' Removes the calling user from a channel.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return validate_response(response).get(key)


@api.route('/api/v1/{channel_type}.rename', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_rename(context, response):
    ''' Changes a channels name.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return validate_response(response).get(key)


@api.route('/api/v1/{channel_type}.setDescription', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_set_description(response):
    ''' Sets a channels description.'''
    return validate_response(response).get('description')


@api.route('/api/v1/{channel_type}.setPurpose', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_set_purpose(response):
    ''' Sets a channels description.'''
    return validate_response(response).get('purpose')


@api.route('/api/v1/{channel_type}.setReadOnly', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_set_readonly(context, response):
    ''' Sets whether a channel is read only or not.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return validate_response(response).get(key)


@api.route('/api/v1/{channel_type}.setTopic', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups', 'im'])
])
def channels_set_topic(response):
    ''' Sets a channels topic.'''
    return validate_response(response).get('topic')


@api.route('/api/v1/{channel_type}.setType', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_set_type(context, response):
    ''' Sets the type of room the channel should be.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return validate_response(response).get(key)


# https://rocket.chat/docs/developer-guides/rest-api/settings


@api.route('/api/v1/settings/{_id}', ['GET', 'POST'])
def setting(response):
    """GET Gets a setting."""
    """POST Updates a setting."""
    return validate_response(response)


# https://rocket.chat/docs/developer-guides/rest-api/users/


@api.route('/api/v1/users.create', ['POST'])
def users_create(response):
    """Create a new user."""
    return validate_response(response)


@api.route('/api/v1/users.createToken', ['POST'])
def users_create_token(response):
    """Create a user authentication token."""
    return validate_response(response)


@api.route('/api/v1/users.delete', ['POST'])
def users_delete(response):
    """Deletes an existing user."""
    return validate_response(response)


@api.route('/api/v1/users.getAvatar', ['POST'])
def users_get_avatar(response):
    """Gets the URL for a user's avatar."""
    return validate_response(response)


@api.route('/api/v1/users.getPresence', ['GET'], params=[
    cosmicray.Param('userId'), cosmicray.Param('username')])
def users_get_presence(response):
    """Gets the online presence of the a user.

    response: { "presence": "offline", "success": true }
    """
    return validate_response(response)


@api.route('/api/v1/users.info', ['GET'], params=[
    cosmicray.Param('userId'), cosmicray.Param('username')])
def users_info(response):
    """Gets a user's information, limited to the caller's permissions.
    { "user": { "_id": "nSYqWzZ4GsKTX4dyK", "type": "user", "status":
    "offline", "active": true, "name": "Example User", "utcOffset": 0,
    "username": "example"  }, "success": true  }
    """
    return validate_response(response).get('user')


@api.route('/api/v1/users.list', ['GET'])
def users_list(response):
    """All of the users and their information, limited to permissions."""
    return validate_response(response).get('users')


@api.route('/api/v1/users.register', ['POST'])
def users_register(response):
    """Register a new user."""
    return validate_response(response)


@api.route('/api/v1/users.resetAvatar', ['POST'])
def users_reset_avatar(response):
    """Reset a user's avatar"""
    return validate_response(response)


@api.route('/api/v1/users.setAvatar', ['POST'])
def users_set_avatar(response):
    """Set a user's avatar"""
    return validate_response(response)


@api.route('/api/v1/users.update', ['POST'])
def users_update(response):
    """Update an existing user."""
    return validate_response(response)


class Token(cosmicray.model.Model):
    __route__ = login
    __slots__ = [
        'authToken',
        'userId'
    ]

    def get_create_payload(self):
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
            data = cosmicray.util.read_artifact_file(fpath, json.loads)
            return Token(**data)
        except:
            pass

    def write_to_storage(self):
        fpath = api.config['AUTH_TOKEN_FILENAME']
        cosmicray.util.write_artifact_file(fpath, self.dict, json.dumps)


class RocketChatError(Exception):
    def __init__(self, error, error_type, status_code):
        message = 'Rocket.Chat Error {!r}: {!r} [!r]'.format(
            error_type, error, status_code)
        super(RocketChatError, self).__init__(message)
