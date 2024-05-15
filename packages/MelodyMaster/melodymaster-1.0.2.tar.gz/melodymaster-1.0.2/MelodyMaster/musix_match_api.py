import requests
import json
import time , os
from .Musix_spot import get_info
class Musix:
    def __init__(self):
        self.token_url = 'https://apic-desktop.musixmatch.com/ws/1.1/token.get?app_id=web-desktop-app-v1.0'
        self.search_term_url = 'https://apic-desktop.musixmatch.com/ws/1.1/track.search?app_id=web-desktop-app-v1.0&page_size=5&page=1&s_track_rating=desc&quorum_factor=1.0'
        self.lyrics_url = 'https://apic-desktop.musixmatch.com/ws/1.1/track.subtitle.get?app_id=web-desktop-app-v1.0&subtitle_format=lrc'
        self.lyrics_alternative = 'https://apic-desktop.musixmatch.com/ws/1.1/macro.subtitles.get?format=json&namespace=lyrics_richsynched&subtitle_format=mxm&app_id=web-desktop-app-v1.0'
        self.token_file = 'musix.txt'

    def get(self, url):
        response = requests.get(url,timeout=25)
        print(response.url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to retrieve data from {url}")

    def get_token(self):
        result = self.get(self.token_url)
        token_json = json.loads(result)
        if token_json['message']['header']['status_code'] == 200:
            current_time = time.time()
            new_token = token_json["message"]["body"]["user_token"]
            expiration_time = current_time + 600
            token_data = {"user_token": new_token, "expiration_time": expiration_time}
            with open(self.token_file, 'w') as file:
                json.dump(token_data, file)
        else:
            raise Exception(result)

    def check_token_expire(self):
        if not self.token_file_exists() or self.token_expired():
            self.get_token()

    def token_file_exists(self):
        return os.path.exists(self.token_file)

    def token_expired(self):
        if self.token_file_exists():
            with open(self.token_file, 'r') as file:
                token_data = json.load(file)
                return token_data['expiration_time'] < time.time()
        return True

    def get_lyrics(self, track_id):
        self.check_token_expire()
        with open(self.token_file, 'r') as file:
            token = json.load(file)['user_token']
        formatted_url = f"{self.lyrics_url}&track_id={track_id}&usertoken={token}"
        result = self.get(formatted_url)
        lyrics = json.loads(result)['message']['body']['subtitle']['subtitle_body']
        return lyrics

    def get_lyrics_alternative(self, title, artist, duration=None):
        self.check_token_expire()
        self.get_info = get_info(f'{title} - {artist}') 
        self.get_id = self.get_info[2]
        self.get_artist = self.get_info[1]
        self.get_title = self.get_info[0]
        with open(self.token_file, 'r') as file:
            self.token = json.load(file)['user_token']
        if ':' in [duration] or duration:
            formatted_url = f"{self.lyrics_alternative}&usertoken={self.token}&q_album=&q_artist={self.get_artist}&q_artists=&track_spotify_id={self.get_id}&q_track={self.get_title}&q_duration={duration}"
        else:
            formatted_url = f"{self.lyrics_alternative}&usertoken={self.token}&q_album=&q_artist={self.get_artist}&q_artists=&track_spotify_id={self.get_id}&q_track={self.get_title}"
        result = self.get(formatted_url)
        lyrics = json.loads(result)['message']['body']['macro_calls']['track.subtitles.get']['message']['body']['subtitle_list'][0]['subtitle']['subtitle_body']
        # print(lyrics)
        return self.get_lrc_lyrics(lyrics)

    def search_track(self, query):
        self.check_token_expire()
        with open(self.token_file, 'r') as file:
            token = json.load(file)['user_token']
        formatted_url = f"{self.search_term_url}&q={query}&usertoken={token}"
        result = self.get(formatted_url)
        list_result = json.loads(result)
        
        if 'track_list' not in list_result['message']['body']:
            raise Exception(result)

        for track in list_result['message']['body']['track_list']:
            track_obj = track['track']
            track_name = f"{track_obj['track_name']} {track_obj['artist_name']}"
            if query in track_name:
                return track_obj['track_id']
        
        return list_result['message']['body']['track_list'][0]['track']['track_id']

    def get_lrc_lyrics(self, lyrics):
        data = json.loads(lyrics)
        lrc = ''
        for item in data:
            minutes = item['time']['minutes']
            seconds = item['time']['seconds']
            hundredths = item['time']['hundredths']
            text = item['text'] if item['text'] else '♪'
            lrc += f"[{minutes:02d}:{seconds:02d}.{hundredths:02d}]{text}\n"
        return lrc

