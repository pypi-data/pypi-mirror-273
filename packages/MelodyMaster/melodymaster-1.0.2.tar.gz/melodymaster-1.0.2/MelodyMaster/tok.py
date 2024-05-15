import requests, os

class Token:
    def __init__(self):
        self.client_id = os.environ['CLIENT_ID'] = '46ac7b073d684c3890e49ac2e42068d8'
        self.client_secret = os.environ['CLIENT_SECERT'] = 'c0d9010101824fedae55b4b2712ea00c'
        self.auth_url = 'https://accounts.spotify.com/api/token'
        self.data = {
    'grant_type': 'client_credentials',
    'client_id': self.client_id,
    'client_secret': self.client_secret,
        }
    @property
    def access_token(self):
        auth_response = requests.post(self.auth_url, data=self.data,timeout=25)
        return auth_response.json().get('access_token')

