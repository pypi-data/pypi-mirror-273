import sys
import os
from pathlib import Path
import requests
from .tok import Token  # تأكد من تصحيح هذا الاستيراد وفقا لهيكل مجلداتك
Token = Token()

def get_info(title: str):
    headers = {
        'accept': '*/*',
        'accept-language': 'en,en-US;q=0.9,ar;q=0.8,en-GB;q=0.7,ar-IQ;q=0.6,zh-CN;q=0.5,zh-MO;q=0.4,zh;q=0.3,ar-AE;q=0.2',
        'authorization': f'Bearer {Token.access_token}' ,
        'referer': 'https://developer.spotify.com/',
        'sec-ch-ua': '"Edge";v="118", "Chromium";v="118", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0',
    }

    params = {
        'q': title,
        'type': 'track',
        'limit': '1',
        'include_external': 'audio',
    }

    response = requests.get('https://api.spotify.com/v1/search', params=params, headers=headers)
    data = response.json()
    duration = data['tracks']['items'][0]['duration_ms']
    name = data['tracks']['items'][0]['name']
    artists = data['tracks']['items'][0]['album']['artists'][0]['name']
    id_ = data['tracks']['items'][0]['id']
    return [name, artists, id_]

