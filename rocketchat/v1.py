import json

import cosmicray


api = cosmicray.Cosmicray('rocketchat')
# ~/.cosmicray/rocketchat
api.config['AUTH_CREDS_FILENAME'] = api.home_dir('creds')
api.config['AUTH_TOKEN_FILENAME'] = api.home_dir('token')


ENTITY_BODY_MAP = {
    'channels': 'channel',
    'groups': 'group',
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


def validate_response(resp):
    if resp.get('status') != 'success':
        raise TypeError('Rocketchat error: {}'.format(resp))
    return resp


@api.route('/api/v1/info', ['GET'])
def info(response):
    return response.json()


@api.route('/api/v1/login', ['POST'])
def login(response):
    '''
    https://docs.rocket.chat/developer-guides/rest-api/authentication/login

    request:
    :param json: { "user": "USERNAME", "password": "PASSWORD" }

    response:
    { "status": "success", "data": { "authToken": "TOKEN", "userId": "USERID" } }
    '''
    return validate_response(response.json()).get('data')


@api.route('/api/v1/logout', ['GET'])
def logout(response):
    '''
    https://docs.rocket.chat/developer-guides/rest-api/authentication/logout

    response:
    { "status": "success", "data": { "message": "You've been logged out!" } }
    '''
    Token.clear_from_storage()
    return validate_response(response.json()).get('data')


@api.route('/api/v1/me', ['GET'])
def me(response):
    '''
    https://docs.rocket.chat/developer-guides/rest-api/authentication/me

    response:
    { "_id": "aobEdbYhXfu5hkeqG", "name": "Example User",
      "emails": [ { "address": "example@example.com", "verified": true } ],
      "status": "offline", "statusConnection": "offline", "username": "example",
      "utcOffset": 0, "active": true, "success": true
    }
    '''
    return response.json()


# https://rocket.chat/docs/developer-guides/rest-api/users/


@api.route('/api/v1/users.create', ['POST'])
def users_create(response):
    """Create a new user."""
    return response.json()


@api.route('/api/v1/users.createToken', ['POST'])
def users_create_token(response):
    """Create a user authentication token."""
    return response.json()


@api.route('/api/v1/users.delete', ['POST'])
def users_delete(response):
    """Deletes an existing user."""
    return response.json()


@api.route('/api/v1/users.getAvatar', ['POST'])
def users_get_avatar(response):
    """Gets the URL for a user's avatar."""
    return response.json()


@api.route('/api/v1/users.getPresence', ['GET'], params=[
    cosmicray.Param('userId'), cosmicray.Param('username')])
def users_get_presence(response):
    """Gets the online presence of the a user.

    response: { "presence": "offline", "success": true }
    """
    return response.json()


@api.route('/api/v1/users.info', ['GET'], params=[
    cosmicray.Param('userId'), cosmicray.Param('username')])
def users_info(response):
    """Gets a user's information, limited to the caller's permissions.
    { "user": { "_id": "nSYqWzZ4GsKTX4dyK", "type": "user", "status":
    "offline", "active": true, "name": "Example User", "utcOffset": 0,
    "username": "example"  }, "success": true  }
    """
    return response.json().get('user')


@api.route('/api/v1/users.list', ['GET'])
def users_list(response):
    """All of the users and their information, limited to permissions."""
    return response.json().get('users')


@api.route('/api/v1/users.register', ['POST'])
def users_register(response):
    """Register a new user."""
    return response.json()


@api.route('/api/v1/users.resetAvatar', ['POST'])
def users_reset_avatar(response):
    """Reset a user's avatar"""
    return response.json()


@api.route('/api/v1/users.setAvatar', ['POST'])
def users_set_avatar(response):
    """Set a user's avatar"""
    return response.json()


@api.route('/api/v1/users.update', ['POST'])
def users_update(response):
    """Update an existing user."""
    return response.json()


# https://rocket.chat/docs/developer-guides/rest-api/im


@api.route('/api/v1/im.messages.others', ['GET'])
def im_messages_others(response):
    """Retrieves the messages from any direct message in the server."""
    return response.json()


@api.route('/api/v1/im.list', ['GET'])
def im_list(response):
    """List the direct channels the caller is part of."""
    return response.json().get('ims')


@api.route('/api/v1/im.list.everyone', ['GET'])
def im_list_everyone(response):
    """List all direct message the caller in the server."""
    return response.json()


# https://rocket.chat/docs/developer-guides/rest-api/livechat


@api.route('/api/v1/livechat/users/{type}/{_id}', ['GET', 'POST', 'DELETE'],
           urlargs=[cosmicray.Param('type', options=['agent', 'department'])])
def livechat_users(response):
    """ GET Get a list of agents or managers. """
    """ POST Create a new livechat agent or manager. """
    """ GET Retrieve agent or manager data. """
    """ DELETE Removes a livechat agent or manager. """
    return response.json()


@api.route('/api/v1/livechat/department/{_id}', ['GET', 'POST', 'PUT', 'DELETE'])
def livechat_department(response):
    """ GET Get a list of livechat departments. info"""
    """ POST Creates a new livechat department. info"""
    """ GET Retrieve a livechat department data. info"""
    """ PUT Updates a livechat department data. info"""
    """ DELETE Delete a livechat department. info"""
    return response.json()


@api.route('/api/v1/livechat/sms-incoming/{service}', ['POST'],
           urlargs=[cosmicray.Param('service', default='twillio', options=['twillio'])])
def livechat_sms_incoming(response):
    """ POST Send SMS messages to Rocket.Chat. info"""
    return response.json()


# https://rocket.chat/docs/developer-guides/rest-api/integration


@api.route('/api/v1/integrations.create', ['POST'])
def integrations_create(response):
    """Creates an integration. Link"""
    return response.json()


@api.route('/api/v1/integrations.list', ['POST'])
def integrations_list(response):
    """Lists all of the integrations. Link"""
    return response.json()


@api.route('/api/v1/integrations.remove', ['POST'])
def integrations_remove(response):
    """Removes an integration. Link"""
    return response.json()



"""
https://docs.rocket.chat/developer-guides/rest-api/chat/
"""


@api.route('/api/v1/chat.getMessage', ['POST'])
def chat_get(response):
    '''Retrieves a single chat message.
    request:
    { "msgId": "7aDSXtjMA3KPLxLjt" }

    response:
    { "message": { "_id": "7aDSXtjMA3KPLxLjt", "rid": "GENERAL",
        "msg": "This is a test!", "ts": "2016-12-14T20:56:05.117Z",
        "u": { "_id": "y65tAmHs93aDChMWu", "username": "graywolf336" } },
      "success": true }
    '''
    return response.json().get('message')


@api.route('/api/v1/chat.postMessage', ['POST'])
def chat_post(response):
    '''Posts a new chat message.

    request:
    { "channel": "#general", "text": "This is a test!" }

    More examples:
    https://docs.rocket.chat/developer-guides/rest-api/chat/postmessage#message-object-example

     '''
    return response.json().get('message')


@api.route('/api/v1/chat.update', ['POST'])
def chat_update(response):
    '''Updates the text of the chat message.'''
    return response.json().get('message')


@api.route('/api/v1/chat.delete', ['POST'])
def chat_delete(response):
    '''Deletes an existing chat message.
    request
    { "roomId": "ByehQjC44FwMeiLbX", "msgId": "7aDSXtjMA3KPLxLjt", "asUser": true }

    response:
    { "_id": "7aDSXtjMA3KPLxLjt", "ts": 1481741940895, "success": true }
    '''
    return response.json()



@api.route('/api/v1/chat.pinMessage', ['POST'])
def chat_pin(response):
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
    return response.json().get('message')


@api.route('/api/v1/chat.react', ['POST'])
def chat_react(response):
    '''Sets/unsets the users reaction to an existing chat message.'''
    return response.json()


@api.route('/api/v1/chat.starMessage', ['POST'])
def chat_star(response):
    '''Stars a chat message for the authenticated user.'''
    return response.json()


@api.route('/api/v1/chat.unPinMessage', ['POST'])
def chat_unpin(response):
    '''Removes the pinned status of the provided chat message.'''
    return response.json()


@api.route('/api/v1/chat.unStarMessage', ['POST'])
def chat_unstar(response):
    '''Removes the star on the chat message for the authenticated user.'''
    return response.json()


"""
https://docs.rocket.chat/developer-guides/rest-api/channels/
"""


@api.route('/api/v1/channels.cleanHistory', ['POST'])
def channels_clean_history(response):
    ''' Cleans up a channels history, requires special permission.'''
    return response.json()



@api.route('/api/v1/channels.list', ['GET'])
def channels_list(response):
    ''' Retrives all of the channels from the server.'''
    return response.json().get('channels')


@api.route('/api/v1/channels.list.joined', ['GET'])
def channels_list_joined(response):
    '''Gets only the channels the calling user has joined.
    https://rocket.chat/docs/developer-guides/rest-api/channels/list-joined/
    '''
    return response.json().get('channels')


@api.route('/api/v1/channels.setJoinCode', ['POST'])
def channels_set_join_code(response):
    ''' Sets the channels code required to join it.'''
    return response.json()


# https://rocket.chat/docs/developer-guides/rest-api/groups


@api.route('/api/v1/groups.list', ['POST'])
def groups_list(response):
    """List the private groups the caller is part of."""
    return response.json()


# Generic definitions for channels, groups, and direct

@api.route('/api/v1/{channel_type}.info', ['GET'], params=[
    # Required (if no roomName) The channels id
    cosmicray.Param('roomId'),
    # Required (if no roomId) The channels name
    cosmicray.Param('roomName')], urlargs=[
        cosmicray.Param('channel_type', options=['channels', 'groups'])])
def channels_info(context, response):
    ''' Gets a channels information.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return response.json().get(key)


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
    """Retrieves the messages from a channel, group, or direct message."""
    messages = response.json().get('messages')
    for message in messages:
        message['channel_type'] = context.urlargs['channel_type']
    return messages


@api.route('/api/v1/{channel_type}.open', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'im', 'groups'])
])
def channels_open(response):
    ''' Adds the channel back to the users list of channels.'''
    return response.json()


@api.route('/api/v1/{channel_type}.close', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups', 'im'])
])
def channels_close(response):
    ''' Removes a channel from a users list of channels.'''
    return response.json()


@api.route('/api/v1/{channel_type}.addAll', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_add_all(response):
    '''
    Adds all of the users on the server to a channel.
    request:
    { "roomId": "ByehQjC44FwMeiLbX", "activeUsersOnly": true|false }
    '''
    return response.json().get('channel')


@api.route('/api/v1/{channel_type}.{action}Moderator', ['POST'], urlargs=[
    cosmicray.Param('action', options=['add', 'remove']),
    cosmicray.Param('channel_type', options=['channels', 'groups'])])
def channels_moderator(response):
    ''' Gives the role of moderator to a user in a channel.'''
    ''' Removes the role of moderator from a user in a channel.'''
    return response.json()


@api.route('/api/v1/{channel_type}.{action}Owner', ['POST'], urlargs=[
    cosmicray.Param('action', options=['add', 'remove']),
    cosmicray.Param('channel_type', options=['channels', 'groups'])])
def channels_owner(response):
    '''Gives the role of owner to a user in a channel.'''
    '''Removes the role of owner from a user in a channel.'''
    return response.json()


@api.route('/api/v1/{channel_type}.create', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_create(context, response):
    '''Creates a new channel.
    https://rocket.chat/docs/developer-guides/rest-api/channels/create/
    '''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return response.json().get(key)


@api.route('/api/v1/{channel_type}.archive', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_archive(response):
    '''Archives a channel.
    https://rocket.chat/docs/developer-guides/rest-api/channels/archive/
    '''
    return response.json()


@api.route('/api/v1/{channel_type}.unarchive', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_unarchive(response):
    '''Unarchives a channel.
    https://rocket.chat/docs/developer-guides/rest-api/channels/unarchive/
    '''
    return response.json()

@api.route('/api/v1/{channel_type}.getIntegrations', ['GET'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_get_integrations(response):
    ''' Gets the channels integration.'''
    return response.json()


@api.route('/api/v1/{channel_type}.invite', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_invite(context, response):
    '''Adds a user to a channel.
    https://rocket.chat/docs/developer-guides/rest-api/channels/invite/
    '''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return response.json().get(key)


@api.route('/api/v1/{channel_type}.kick', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_kick(context, response):
    ''' Removes a user from a channel.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return response.json().get(key)


@api.route('/api/v1/{channel_type}.leave', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_leave(context, response):
    ''' Removes the calling user from a channel.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return response.json().get(key)


@api.route('/api/v1/{channel_type}.rename', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_rename(context, response):
    ''' Changes a channels name.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return response.json().get(key)


@api.route('/api/v1/{channel_type}.setDescription', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_set_description(response):
    ''' Sets a channels description.'''
    return response.json().get('description')


@api.route('/api/v1/{channel_type}.setPurpose', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_set_purpose(response):
    ''' Sets a channels description.'''
    return response.json().get('purpose')


@api.route('/api/v1/{channel_type}.setReadOnly', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_set_readonly(context, response):
    ''' Sets whether a channel is read only or not.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return response.json().get(key)


@api.route('/api/v1/{channel_type}.setTopic', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups', 'im'])
])
def channels_set_topic(response):
    ''' Sets a channels topic.'''
    return response.json().get('topic')


@api.route('/api/v1/{channel_type}.setType', ['POST'], urlargs=[
    cosmicray.Param('channel_type', options=['channels', 'groups'])
])
def channels_set_type(context, response):
    ''' Sets the type of room the channel should be.'''
    key = ENTITY_BODY_MAP.get(context.urlargs['channel_type'])
    return response.json().get(key)


# https://rocket.chat/docs/developer-guides/rest-api/settings


@api.route('/api/v1/settings/:_id', ['GET', 'POST'])
def setting(response):
    """GET Gets a setting."""
    """POST Updates a setting."""
    return response.json()


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
