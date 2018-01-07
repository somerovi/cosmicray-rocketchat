from . import v1, models
from .__version__ import __version__


def monkey_patch_ssl():
    if not v1.api.get_config('verify'):
        # If you run a private server with self signed certificate,
        # you'll want to disable ssl validation
        import requests
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings()


def configure(monkey_patch=False, config=None, **kwargs):
    if monkey_patch:
        monkey_patch_ssl()
    if not config:
        config = {}
    config['monkey_patch'] = monkey_patch
    v1.api.configure(config=config, **kwargs)


def create_creds_file(username, password):
    import json
    import cosmicray

    fpath = v1.api.get_config('AUTH_CREDS_FILENAME')
    cosmicray.util.write_artifact_file(
        fpath, {'user': username, 'password': password}, json.dumps)
    print('Credentials stored in {}'.format(fpath))


def set_creds_env(username, password):
    import os
    os.environ['ROCKETCHAT_USER'] = username
    os.environ['ROCKETCHAT_PASSWORD'] = password


def load_config():
    v1.api.load_configurations()
    if v1.api.get_config('monkey_patch'):
        monkey_patch_ssl()

def store_config():
    v1.api.store_configurations()


def debug(enable=True):
    configure(config={'debug': enable})


def channels():
    return dict((c.name, c) for c in models.Channel.channels)


def groups():
    return dict((c.name, c) for c in models.Channel.groups)


def direct():
    return dict((c._id, c) for c in models.Channel.direct)


def users():
    return dict((u.username, u) for u in models.User.users)


configure(authenticator=v1.authenticator)
load_config()
