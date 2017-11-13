import cosmicray
import json
import rocketchat


if __name__ == '__main__':
    rocketchat.configure(
        domain='https://mydomain.com',
        verify_ssl=True)
    creds_file = rocketchat.api.config['AUTH_CREDS_FILENAME']
    print(creds_file)
    cosmicray.util.write_artifact_file(
        creds_file, json.dumps({
            'user': 'myusername',
            'password': 'mysecretpassword'
        }))
    print(rocketchat.channels.list_all.get())
