from .api import api, login, logout, me, info, authenticator
from . import channels


def monkey_patch_ssl():
    # If you run a private server with self signed certificate,
    # you'll want to disable ssl validation
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings()


def configure(domain, verify_ssl=True):
    if not verify_ssl:
        monkey_patch_ssl()
    api.configure(domain=domain, authenticator=authenticator, verify=verify_ssl)


__all__ = ['api', 'configure', 'login', 'logout', 'me', 'info', 'channels']
