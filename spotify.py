import base64
import requests
import json
import os
from dotenv import load_dotenv
#https://developer.spotify.com/documentation/web-api/reference
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
print(client_id)

# if True:
#     url = 'https://accounts.spotify.com/authorize'
#     params = {
#     "client_id":"8e83bb690586463982d64a1f7cc66e21",
#     "response_type":"code",
#     "redirect_uri":"https://juliasusser.com/",
#     "scope":"user-read-private%20user-read-email&state=34fFs29kd09"
#     }
#     r = requests.get(url, params=params)
#     print(r)
code = 'AQCGm4Ul9bBM-y2gHEQEpHTNtnbuFfvwQv2pFp-gpY_c3q4ZDeHLC9xtd0eEH58U9nInA_hPU4B1Kx0lRKvgZXbBcQ1-MqdngPOujHtlyXqbEkJtPR8rUVTZ1DUOkwxV8K843R-PFTEa9Hg4pb3KVW8-g5bXTJjuPjVPPhMeUOiWMEcy9x2oxeIsPhcX6vdk79Mx6pRG6dBrY3im5zu1Bx2uwTyLzhQj'
class Spotify:
    def __init__(self):

        # self.getCode()
        #self.getToken()
        self.refreshToken()
        #self.createPlaylist()
        #self.addSongs()
        #self.getLikedSongs()
        #self.SearchSpotify()
    def getCode(self):
        url = 'https://accounts.spotify.com/authorize?client_id='+client_id+'&response_type=code&redirect_uri=https://juliasusser.com/&scope=playlist-modify-private user-library-read'
        print(url)
    def getBase64(self):
        message = client_id + ':' + client_secret
        message = message.encode('ascii')
        value = base64.b64encode(message)
        return value
    def getToken(self):
        url = 'https://accounts.spotify.com/api/token'
        string = "Basic "+ self.getBase64().decode("utf-8")
        headers = {"Authorization": string}
        data  = {
            'grant_type' : 'authorization_code',
            'code' : code,
            'redirect_uri' : "https://juliasusser.com/",
            "client_secret": client_secret,
             "client_id":  client_id
            }

        r = requests.post(url, headers=headers, data=data)
        token = r.json()
        print(token)
        file = open("token.json", "w")
        json.dump(token,file)
    def refreshToken(self):
        file = open("token.json", "r")
        token = json.load(file)
        url = 'https://accounts.spotify.com/api/token'
        string = "Basic "+ self.getBase64().decode("utf-8")
        headers = {"Authorization": string}
        data  = {
            'grant_type' : 'refresh_token',
            'refresh_token' : token["refresh_token"],
            }

        r = requests.post(url, headers=headers, data=data)
        token = r.json()
        self.token = token['access_token']

    def createPlaylist(self):
        user_id = "pmfqzviblemqox2dsmzed9l31"
        url = "https://api.spotify.com/v1/users/"+user_id+"/playlists"
        headers = {"Authorization": "Bearer "+self.token, "Accept": "application/json", "Content-Type": "application/json"}
        data  = json.dumps({
            "name":"Newer Playlist",
            "description":"New playlist description",
            "public":"false"
            })

        r = requests.post(url, headers=headers, data=data)
        response = r.json()
        print(response)
    def addSongs(self):
        playlist_id = "2Cpu742jFdXti8mCxCbcmV"
        url = "https://api.spotify.com/v1/playlists/"+playlist_id+"/tracks"
        headers = {"Authorization": "Bearer "+self.token, "Accept": "application/json", "Content-Type": "application/json"}
        data  = json.dumps({
            "uris":["spotify:track:0VjIjW4GlUZAMYd2vXMi3b"]
            })

        r = requests.post(url, headers=headers, data=data)
        response = r.json()
        print(response)
    def getLikedSongs(self):

        url = "https://api.spotify.com/v1/me/tracks"
        headers = {"Authorization": "Bearer "+self.token}

        r = requests.get(url, headers=headers)
        print(r)
        response = r.json()
        print(response)
    def SearchSpotify(self):
        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": "Bearer "+self.token}
        data = {
        "q":"roadhouse%20blues",
        "type":["album","track"]
        }
        r = requests.get(url, headers=headers,params=data)
        print(r)
        response = r.json()
        print(response)

obj = Spotify()
