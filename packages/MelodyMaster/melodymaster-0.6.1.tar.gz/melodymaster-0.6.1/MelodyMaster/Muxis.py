import argparse
import asyncio
import re
from .musix_match_api import Musix 
from collections import OrderedDict
import json
import os
import speech_recognition as sr
from pydub import AudioSegment
musix = Musix()
black_space = ['"""""', '', '♪', ' """""']
author = 'https://OverGroundOfWall.t.me'

async def get_default_lyrics(query, srt):
    try: 
        dic = OrderedDict({'lyrics': ""})
        dic['info'] = {
            'Dev': '~ ZHAN',
            'my_account': f'{author}'  
        }
        track_id = musix.search_track(query)
        response = musix.get_lyrics(track_id)
        for line in response.strip().splitlines():
            match = re.findall(r'\[(.*?)\](.*?)$', line)
            time, content = match[0][0].split('.')[0], match[0][1]
            if content not in black_space:
                if srt == 'true':
                    dic['lyrics'] += f"[{time}] {content}\n"
                elif srt == 'false' or srt == None or srt == '' or srt == ' ':
                    dic['lyrics'] += f"{content}\n"

        print(json.dumps(dic, ensure_ascii=False, indent=4))
                    
    except Exception as e:
        print({"error": "Track ID not found.", "isError": True, "SynTex": f"{e}" , 'status_code' : 404})

async def get_alternative_lyrics(title,artist,duration,srt):
    print(srt)
    if srt == 'false' or srt == None or srt == '' or srt == ' ':
        try:
            if duration or ':' in [duration]:
                dic = OrderedDict({'lyrics':[]})
                dic['info'] = {
                    'Dev':'~ ZHAN',
                    'my_account':f'{author}'  
                    }
                lyrics = musix.get_lyrics_alternative(title, artist, convert_duration(duration))
                for lyr in lyrics.strip().splitlines():
                    match = re.findall(r'\[(.*?)\](.*?)$', lyr)
                    time, content = match[0][0].split('.')[0], match[0][1]
                    time = time[-4:] if time[0] == '0' else time
                    if content not in black_space:
                        dic['lyrics'].append({time:content})
                return print(dic)
            else:
                dic = OrderedDict({'lyrics':[]})
                dic['info'] = {
                    'Dev':'~ ZHAN',
                    'my_account':f'{author}'  
                    }
                lyrics = musix.get_lyrics_alternative(title,artist)
                for lyr in lyrics.strip().splitlines():
                    match = re.findall(r'\[(.*?)\](.*?)$', lyr)
                    time, content = match[0][0].split('.')[0], match[0][1]
                    time = time[-4:] if time[0] == '0' else time
                    if content not in black_space:
                        dic['lyrics'].append({time:content})
                return print(dic)
        except Exception:
            return print({'status_code': 404,"error": "Lyrics not found.", "isError": True, "title": title, "artist": artist, "duration": duration})
    elif srt == 'true':
        try:
            print(duration)
            if duration or ':' in [duration]:
                dic = OrderedDict({'lyrics':[]})
                dic['info'] = {
                    'Dev':'~ ZHAN',
                    'my_account':f'{author}'  
                    }
                lyrics = musix.get_lyrics_alternative(title, artist, convert_duration(duration))
                for lyr in lyrics.strip().splitlines():
                    match = re.findall(r'\[(.*?)\](.*?)$', lyr)
                    time, content = match[0][0], match[0][1]
                    if content not in black_space:
                        dic['lyrics'].append({time:content})
                return print(dic)
            else:
                dic = OrderedDict({'lyrics':[]})
                dic['info'] = {
                    'Dev':'~ ZHAN',
                    'my_account':f'{author}'  
                    }
                lyrics = musix.get_lyrics_alternative(title,artist)
                for lyr in lyrics.strip().splitlines():
                    match = re.findall(r'\[(.*?)\](.*?)$', lyr)
                    time, content = match[0][0] , match[0][1]
                    if content not in black_space:
                        dic['lyrics'].append({time:content})
                return print(dic)
        except Exception:
            return print({'status_code': 404,"error": "Lyrics not found.", "isError": True, "title": title, "artist": artist, "duration": duration})
    else:
        return print({'status_code': 404,"error": "Lyrics not found.", "isError": True, "title": title, "artist": artist, "duration": duration})
def convert_duration(time):
    minutes, seconds = map(int, time.split(":"))
    total_seconds = (minutes * 60) + seconds
    return total_seconds

def prepare_voice_file(path: str) -> str:
    """
    Converts the input audio file to WAV format if necessary and returns the path to the WAV file.
    """
    if os.path.splitext(path)[1] == '.wav':
        return path
    elif os.path.splitext(path)[1] in ('.mp3', '.m4a', '.ogg', '.flac'):
        audio_file = AudioSegment.from_file(
            path, format=os.path.splitext(path)[1][1:])
        wav_file = os.path.splitext(path)[0] + '.wav'
        audio_file.export(wav_file, format='wav')
        return wav_file
    else:
        raise ValueError(
            f'Unsupported audio format: {format(os.path.splitext(path)[1])}')


def transcribe_audio(audio_data, language) -> str:
    """
    Transcribes audio data to text using Google's speech recognition API.
    """
    r = sr.Recognizer()
    text = r.recognize_google(audio_data, language=language)
    return text


def write_transcription_to_file(text, output_file) -> None:
    """
    Writes the transcribed text to the output file.
    """
    with open(output_file, 'w') as f:
        f.write(text)


async def recognize_text(input_path: str, language: str) -> None:
    """
    Transcribes an audio file at the given path to text and writes the transcribed text to the output file.
    """
    try:
        wav_file = prepare_voice_file(input_path)
        with sr.AudioFile(wav_file) as source:
            audio_data = sr.Recognizer().record(source)
            text = transcribe_audio(audio_data, language)
            result = {"speech": text}
            print(json.dumps(result))
            os.remove(input_path)
            os.remove(wav_file)
    except Exception as e:
        error_result = {
            "error": "An error occurred",
            "message": str(e)
        }
        os.remove(input_path)
        os.remove(wav_file)
        print(json.dumps(error_result))

def get_default_lyrics_from_command_line():
    parser = argparse.ArgumentParser(description='Recognize song using Shazam.')
    parser.add_argument('file', type=str, help='Path to the audio file')
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(get_default_lyrics(args.file))

def get_alternative_lyrics_from_command_line():
    parser = argparse.ArgumentParser(description='Recognize song using Shazam.')
    parser.add_argument('file', type=str, help='Path to the audio file')
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(get_alternative_lyrics(args.file))

def recognize_text_from_command_line():
    parser = argparse.ArgumentParser(description='Recognize song using Shazam.')
    parser.add_argument('file', type=str, help='Path to the audio file')
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(recognize_text(args.file))
    
if __name__ == '__main__':
    get_alternative_lyrics_from_command_line()
    get_default_lyrics_from_command_line()
    recognize_text_from_command_line()
