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


def load_config():
    v1.api.load_configurations()
    if v1.api.get_config('monkey_patch'):
        monkey_patch_ssl()

def store_config():
    v1.api.store_configurations()


configure(authenticator=v1.authenticator)
load_config()
