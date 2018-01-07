Cosmicray-Rocketchat
====================

-----------------------------------------
Implementation of Rocket.Chat restful api
-----------------------------------------

.. warning::

   Cosmicray-Rocketchat is under development


Install
-------

.. code::

   $ pip install cosmicray-rocketchat


Quick start
-----------

CLI
===

Cosmicray-Rocketchat ships with a simple commandline interface.

.. code::

   $ rocketchat --help


Configuration: Credentials
==========================

Credentials are stored in a file called `~/.cosmicray/rocketchat/creds`. The following snippet of code creates it:

.. code:: python

    >>> import rocketchat
    >>> rocketchat.create_creds_file('myusername', 'mypassword')


Configuration: Domain and other settings
========================================

The following code will configure cosmicray-rocketchat client with the domain to use and save the configuration to file

.. code:: python

   >>> import rocketchat
   >>> rocketchat.configure(domain='http://myrocketchatdomain.com')
   >>> rocketchat.store_config()

When importing cosmicray-rocketchat, the config will be automatically loaded. If you need to disable ssl verification

.. code:: python

    >>> rocketchat.configure(
    ...    monkey_patch=True,
    ...    verify=False)
    >>> rocketchat.store_config()

The `monkey_patch` flag disable SSL warnings.

Alternatively, the above configurations can be changed using the cli:

.. code::

   $ rocketchat configure password --username myusername
   Promp password:
   $ rocketchat configure domain "http://myrocketchatdomain.com" --no-verify


Configuration: Debugging
========================

If there are any issues with making the requests, debugging can be enabled:

.. code:: python

   >>> import rocketchat
   >>> rocketchat.configure(config={'debug': True})

Or via command line:

.. code::

   $ rocketchat configure domain --verbose


API
===

Cosmicray-Rocketchat defines endpoints from https://rocket.chat/docs/developer-guides/rest-api in `rocketchat.v1` module. For example, to get the server api version, you would make the following request:

.. code:: python
   >>> import rocketchat
   >>> rocketchat.v1.info().get()

The preferred way to interact with the Rocket.Chat api is to use models defined in `rocketchat.models` module.

.. code:: python

   >>> rocketchat.models.User.me
   <User(_id='CA9t5phAAaLcN9sdZ', type=None, status='offline', active=True, name='bot'...)>
   >>> foo = rocketchat.models.User(username='foo').get()
   >>> foo.send('Hello foo')


To list public, groups, direct message rooms

.. code:: python

   >>> rooms = rocketchat.models.Channel.channels
   >>> groups = rocketchat.models.Channel.groups
   >>> direct = rocketchat.models.Channel.direct

For convenience, one could access users and rooms via mappings:

.. code:: python

   >>> users = rocketchat.users()
   >>> channels = rocketchat.channels()
   >>> groups = rocketchat.groups()
   >>> foo = users['foo']
   >>> foo.send('Hello Foo!')
   >>> messages = channels['mychannel'].messages.unread
   >>> channels['mychannel'].send('Hey!')


To list/send messages for a channel (direct, group, or public/private channel):

.. code:: python

   >>> myroom = rocketchat.channels()['myroom']
   >>> print(myroom.messages.unread)
   >>> messages = myroom.messages.by_daterange('2018-01-01', '2018-01-02').count(100).get()
   >>> myroom.send('hello')


To update/delete messages:

.. code:: python

   >>> message = myroom.messages.last[0]
   >>> message.msg = 'changed message'
   >>> message.update()
   >>> message.pin()
   >>> message.delete()
