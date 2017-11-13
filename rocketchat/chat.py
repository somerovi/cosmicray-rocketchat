"""
https://docs.rocket.chat/developer-guides/rest-api/chat/
"""

import cosmicray

from cosmicray.util import param

from .api import api


@api.route('/api/v1/chat.delete', ['POST'])
def delete(request):
    '''Deletes an existing chat message.
    request
    { "roomId": "ByehQjC44FwMeiLbX", "msgId": "7aDSXtjMA3KPLxLjt", "asUser": true }

    response:
    { "_id": "7aDSXtjMA3KPLxLjt", "ts": 1481741940895, "success": true }
    '''
    return request.map_model(request.response.json())


@api.route('/api/v1/chat.getMessage', ['POST'])
def get_message(request):
    '''Retrieves a single chat message.
    request:
    { "msgId": "7aDSXtjMA3KPLxLjt" }

    response:
    { "message": { "_id": "7aDSXtjMA3KPLxLjt", "rid": "GENERAL",
        "msg": "This is a test!", "ts": "2016-12-14T20:56:05.117Z",
        "u": { "_id": "y65tAmHs93aDChMWu", "username": "graywolf336" } },
      "success": true }
    '''
    return request.map_model(request.response.json())


@api.route('/api/v1/chat.pinMessage', ['POST'])
def pin_message(request):
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
    return request.map_model(request.response.json())


@api.route('/api/v1/chat.postMessage', ['POST'])
def post_message(request):
    '''Posts a new chat message.

    request:
    { "channel": "#general", "text": "This is a test!" }

    More examples:
    https://docs.rocket.chat/developer-guides/rest-api/chat/postmessage#message-object-example

     '''
    return request.map_model(request.response.json())


@api.route('/api/v1/chat.react', ['POST'])
def react(request):
    '''Sets/unsets the users reaction to an existing chat message.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/chat.starMessage', ['POST'])
def start_message(request):
    '''Stars a chat message for the authenticated user.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/chat.unPinMessage', ['POST'])
def unpin_message(request):
    '''Removes the pinned status of the provided chat message.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/chat.unStarMessage', ['POST'])
def unstart_message(request):
    '''Removes the star on the chat message for the authenticated user.'''
    return request.map_model(request.response.json())


@api.route('/api/v1/chat.update', ['POST'])
def update(request):
    '''Updates the text of the chat message.'''
    return request.map_model(request.response.json())
