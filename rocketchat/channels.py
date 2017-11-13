"""
https://docs.rocket.chat/developer-guides/rest-api/channels/
"""

import cosmicray

from cosmicray.util import param

from .api import api


@api.route('/api/v1/channels.addAll', ['POST'])
def add_all(request):
    '''
    Adds all of the users on the server to a channel.
    request:
    { "roomId": "ByehQjC44FwMeiLbX", "activeUsersOnly": true|false }
    '''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.addModerator', ['POST'])
def add_moderator(request):
    ''' Gives the role of moderator to a user in a channel.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.addOwner', ['POST'])
def add_owner(request):
    ''' Gives the role of owner to a user in a channel.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.archive', ['POST'])
def archive(request):
    ''' Archives a channel.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.cleanHistory', ['POST'])
def clean_history(request):
    ''' Cleans up a channels history, requires special permission.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.close', ['POST'])
def close(request):
    ''' Removes a channel from a users list of channels.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.create', ['POST'])
def create(request):
    ''' Creates a new channel.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.getIntegrations', ['GET'])
def get_integrations(request):
    ''' Gets the channels integration.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.history', ['GET'], params=[
    # Required The channels id
    param('roomId', required=True),
    # Optional Default: now The end of time range of messages to retrieve
    param('latest'),
    # Optional Default: n/a The start of the time range of messages to retrieve
    param('oldest'),
    #Optional Default: false Whether messages which land on latest and oldest should be included
    param('inclusive'),
    # Optional Default: 20 The amount of messages to retrieve
    param('count'),
    # Optional Default: false Whether the amount of unreads should be included.
    param('unreads')
])
def history(request):
    ''' Retrieves the messages from a channel.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.info', ['GET'], params=[
    # Required (if no roomName) The channels id
    param('roomId'),
    # Required (if no roomId) The channels name
    param('roomName')
])
def info(request):
    ''' Gets a channels information.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.invite', ['POST'])
def invite(request):
    ''' Adds a user to a channel.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.kick', ['POST'])
def kick(request):
    ''' Removes a user from a channel.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.leave', ['POST'])
def leave(request):
    ''' Removes the calling user from a channel.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.list', ['GET'])
def list_all(request):
    ''' Retrives all of the channels from the server.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.list.joined', ['GET'])
def list_joined(request):
    ''' Gets only the channels the calling user has joined.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.open', ['POST'])
def join(request):
    ''' Adds the channel back to the users list of channels.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.removeModerator', ['POST'])
def remove_moderator(request):
    ''' Removes the role of moderator from a user in a channel.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.removeOwner', ['POST'])
def remove_owner(request):
    ''' Removes the role of owner from a user in a channel.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.rename', ['POST'])
def rename(request):
    ''' Changes a channels name.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.setDescription', ['POST'])
def set_description(request):
    ''' Sets a channels description.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.setJoinCode', ['POST'])
def set_join_code(request):
    ''' Sets the channels code required to join it.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.setPurpose', ['POST'])
def set_purpose(request):
    ''' Sets a channels description.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.setReadOnly', ['POST'])
def set_readonly(request):
    ''' Sets whether a channel is read only or not.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.setTopic', ['POST'])
def set_topic(request):
    ''' Sets a channels topic.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.setType', ['POST'])
def set_type(request):
    ''' Sets the type of room the channel should be.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/channels.unarchive', ['POST'])
def unarchive(request):
    ''' Unarchives a channel.'''
    return request.map_model(request.response.json())
