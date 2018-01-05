import datetime

import cosmicray

from cosmicray import model

from . import v1


class Base(model.Model):
    __ignore__ = ['success']


class User(Base):
    __slots__ = [
        "_id",
        "type",
        "status",
        "active",
        "name",
        "utcOffset",
        "username",
        # Admin specific
        "createdAt",
        "lastLogin",
        "services",
        "email",
        "emails",
        "resume",
        "roles",
        "statusConnection",
        "settings",
        "language",
        "bot",
        # Non-API fields
        '_direct'
    ]
    __route__ = v1.users_info

    me = model.relationship(
        'User', v1.me, is_static=True)
    channels =  model.relationship(
        'Channel', v1.channels_list_joined, is_sequence=True, is_static=True)
    users = model.relationship(
        'User', v1.users_list, is_sequence=True, is_static=True)

    def get(self):
        params = {'userId': self._id} if self._id else {'username': self.username}
        self.dict = self(params=params).get().dict
        return self

    def send(self, text, alias=None, emoji=None, avatar=None, attachments=None):
        return self.direct.send(
            text, alias=alias, emoji=emoji, avatar=avatar, attachments=attachments)

    @property
    def direct(self):
        '''
        Open direct message with the given user
        '''
        if self._direct is None:
            if self._id is None:
                self.get()
            self._direct = self._get_direct_room()
            if self._direct is None:
                try:
                    d = Direct(_id=self._id).open()
                except Exception as error:
                    # returns 400 if room is already opened
                    pass
                self._direct = self._get_direct_room()
        return self._direct

    def _get_direct_room(self):
        try:
            Channel.direct.clear()
            return next(u for u in Channel.direct if self.username in u.usernames)
        except StopIteration:
            pass

    def __eq__(self, obj):
        if isinstance(obj, User):
            return self._id == obj._id
        return obj.get('_id') == self._id


class Channel(Base):
    CHANNEL_TYPE = 'channels'

    __slots__ = [
        '_id',
        'name',
        't',
        'usernames',
        'msgs',
        'u',
        'ts',
        'ro',
        'sysMes',
        '_updatedAt',
        'customFields',
        'lm',
        'username',
        'topic',
        'default',
        'archived',
        # Non-api fields
        'channel_type'
    ]
    __route__ = v1.channels_info

    channels = model.relationship(
        'Channel', v1.channels_list,
        urlargs={'channel_type': 'channels'},
        is_sequence=True, is_static=True)
    direct = model.relationship(
        'Direct', v1.channels_list,
        urlargs={'channel_type': 'im'},
        is_sequence=True, is_static=True)
    groups = model.relationship(
        'Group', v1.channels_list,
        urlargs={'channel_type': 'groups'},
        is_sequence=True, is_static=True)
    _messages = model.relationship(
        'Message', v1.channels_messages, is_sequence=True,
        params={'roomId': model.ModelParam('_id')},
        urlargs={'channel_type': model.ModelParam('CHANNEL_TYPE')},
        lazy=True)

    @property
    def messages(self):
        return Messages(channel=self)

    @property
    def users(self):
        return list(User(username=username).get() for username in self.usernames)

    @property
    def configuration(self):
        identifier = '{}:{}'.format(self._id, self.name or '')
        v1.api.config.setdefault(identifier, {})
        return v1.api.config[identifier]

    def get(self):
        params = {'roomId': self._id} if self._id else {'roomName': self.name}
        self.channel_type = self.CHANNEL_TYPE
        self.dict = self(params=params).get().dict
        return self

    def add_all(self, active_users_only=False):
        return v1.channels_add_all(**self.get_payload(
            {'activeUsersOnly': active_users_only}),
            urlargs={'channel_type': self.CHANNEL_TYPE}).post()

    def invite(self, user=None, userid=None, username=None):
        userid = user and user._id or userid or User(username=username).get()._id
        return v1.channels_invite(
            self.__class__, **self.get_payload({'userId': userid}),
            urlargs={'channel_type': self.CHANNEL_TYPE}).post()

    def kick(self, user=None, userid=None, username=None):
        userid = user and user._id or userid or User(username=username).get()._id
        return v1.channels_kick(
            self.__class__, **self.get_payload({'userId': userid}),
            urlargs={'channel_type': self.CHANNEL_TYPE}).post()

    def open(self):
        return v1.channels_open(
            **self.get_payload(),
            urlargs={'channel_type': self.CHANNEL_TYPE}).post()

    def close(self):
        return v1.channels_close(
            **self.get_payload(),
            urlargs={'channel_type': self.CHANNEL_TYPE}).post()

    def leave(self):
        return v1.channels_leave(
            self.__class__, **self.get_payload(),
            urlargs={'channel_type': self.CHANNEL_TYPE}).post()

    def create(self):
        return v1.channels_create(Channel, json={
            'name': self.name,
            'members': self.usernames,
            'readOnly': True if self.ro else False
        }, urlargs={'channel_type': self.CHANNEL_TYPE}).post()

    def update(self):
        pass

    def delete(self):
        return v1.channels_archive(
            **self.payload(),
            urlargs={'channel_type': self.CHANNEL_TYPE}).post()

    def send(self, text, alias=None, emoji=None, avatar=None, attachments=None):
        return Message(msg=text, rid=self._id,
                       alias=alias, emoji=emoji, avatar=avatar,
                       attachments=attachments).create()

    def get_payload(self, args=None, **kwargs):
        payload = {'roomId': self._id}
        print(payload)
        payload.update(args or {}, **kwargs)
        return {'json': payload}


class Direct(Channel):
    CHANNEL_TYPE = 'im'


class Group(Channel):
    CHANNEL_TYPE = 'groups'


class Message(Base):
    __slots__ = [
        '_id',
        'rid',
        'msg',
        'ts',
        'u',
        '_updatedAt',
        'attachments',
        'groupable',
        'parseUrls',
        'alias',
        'channels',
        'mentions',
        'bot',
        'urls',
        't',
        'groupable',
        'pinned',
        'pinnedAt',
        'pinnedBy',
        'editedBy',
        'editedAt',
        # Non-API fields
        'emoji',
        'avatar',
        'channel_name',
        'channel_type',
        'unreadNotLoaded'
    ]

    @property
    def user(self):
        return User(_id=self.u['_id']).get()

    @property
    def user_mentions(self):
        return list(User(**m) for m in self.mentions)

    @property
    def channel(self):
        if self.channel_type == 'channels':
            return Channel(_id=self.rid, channel_type=self.channel_type).get()
        elif self.channel_type == 'groups':
            return Group(_id=self.rid, channel_type=self.channel_type).get()
        else:
            return Direct(_id=self.rid, channel_type=self.channel_type)

    def get(self):
        self.dict = v1.message_get(Message, **self.get_payload()).post()
        return self

    def update(self):
        return v1.message_update(
            Message,
            **self.get_payload({
            'roomId': self.rid,
            'text': self.msg
        })).post()

    def create(self):
        channel = '#{}'.format(self.channel_name) if self.channel_name else None,
        return v1.message_post(
            Message,
            **self.get_payload({
                'roomId': self.rid,
                #'channel': channel,
                'text': self.msg,
                'alias': self.alias,
                'emoji': self.emoji,
                'avatar': self.avatar,
                'attachments': self.attachments
        })).post()

    def delete(self, as_user=True):
        return v1.message_delete(**self.get_payload({
            'roomId': self.rid,
            'text': self.msg,
            'asUser': as_user
        })).post()

    def pin(self):
        return v1.message_pin(Message, **self.get_payload()).post()

    def unpin(self):
        return v1.message_unpin(**self.get_payload()).post()

    def react(self):
        # Not supported yet?
        return v1.message_react(**self.get_payload({
            'emoji': self.emoji
        })).post()

    def unreact(self):
        # Not supported yet?
        return v1.message_unreact(**self.get_payload()).post()

    def get_payload(self, args=None, **kwargs):
        payload = {'msgId': self._id, 'messageId': self._id}
        payload.update(args or {}, **kwargs)
        return {'json': payload}


class Messages(object):

    def __init__(self, channel, params=None, sort_order='asc'):
        self.channel = channel
        self.params = params or {}
        self.sort_order = sort_order

    def get_params(self, **kwargs):
        params = dict(self.params)
        params.update(**kwargs)
        return params

    @property
    def recent(self):
        return self._sort(self.get())

    @property
    def last(self):
        return self.count(1).get()

    @property
    def today(self):
        pass

    @property
    def unread(self):
        last_message_dt = self.channel.configuration.get(
            'last_message_dt', '2017-01-01')

        messages = self.include_unread_count\
                       .count(1)\
                       .by_daterange(last_message_dt, None)\
                       .get()
        if messages:
            recent_message_dt = messages[0].ts
            unread = messages[0].unreadNotLoaded
            if unread:
                messages.extend(self.count(unread)\
                               .by_daterange(last_message_dt, recent_message_dt)\
                               .get())
            self.channel.lm = messages[0]._updatedAt
            self.channel.configuration['last_message_dt'] = messages[0]._updatedAt
            v1.api.store_configurations()
        return self._sort(messages)

    @property
    def asc(self):
        return Messages(self.channel, self.get_params(), 'asc')

    @property
    def desc(self):
        return Messages(self.channel, self.get_params(), 'desc')

    @property
    def inclusive(self):
        return Messages(
            self.channel, self.get_params(inclusive=True), self.sort_order)

    @property
    def include_unread_count(self):
        return Messages(
            self.channel, self.get_params(unreads=True), self.sort_order)

    def count(self, count):
        return Messages(
            self.channel, self.get_params(count=count), self.sort_order)

    def by_daterange(self, start, end):
        return Messages(
            self.channel, self.get_params(oldest=start, latest=end), self.sort_order)

    def _sort(self, messages):
        return sorted(
            messages, key=lambda obj: obj.ts, reverse=self.sort_order == 'desc')

    def get(self):
        return list(self.channel._messages(params=self.params).get())

    def delete(self):
        if 'oldest' not in self.params or 'latest' not in self.params:
            raise TypeError('Missing required parameters: oldest/latest')
        return v1.channels_remove_messages(json={
            'roomId': self.channel._id,
            'oldest': self.params['start'],
            'latest': self.param['end'],
            'inclusive': self.param.get('inclusive', False)
        }).post()
