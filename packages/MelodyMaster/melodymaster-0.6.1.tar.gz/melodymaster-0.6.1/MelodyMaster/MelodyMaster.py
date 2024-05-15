import argparse
import asyncio
import logging
import json
from aiohttp_retry import ExponentialRetry
from MelodyMaster import Shazam, Serialize, HTTPClient
from pprint import pprint


async def recognize_song_te(file_path):
    shazam = Shazam(
        http_client=HTTPClient(
            retry_options=ExponentialRetry(
                attempts=12, max_timeout=204.8, statuses={500, 502, 503, 504, 429}
            ),
        ),
    )

    result = await shazam.recognize(file_path)
    json_data = json.dumps(result, indent=4)
    print(json_data)

async def search_album_te(album_id):
    shazam = Shazam()
    albums = await shazam.search_album(album_id=album_id)
    serialized = Serialize.album_info(data=albums)

    for i in serialized.data[0].relationships.tracks.data:
        msg = (
            f"{i.id} | {i.attributes.album_name} | {i.attributes.artist_name} [{i.attributes.name}]"
        )
        print(msg)

async def recognize_and_search_te(file_path):
    shazam = Shazam(
        http_client=HTTPClient(
            retry_options=ExponentialRetry(
                attempts=12, max_timeout=204.8, statuses={500, 502, 503, 504, 429}
            ),
        ),
    )

    # Recognize song
    new_version_path = await shazam.recognize(file_path)

    # Search for album
    album_info = await shazam.search_album(album_id=new_version_path["track"]["albumadamid"])
    album_serialized = Serialize.album_info(data=album_info)

    # Print album name
    print(album_serialized.data[0].attributes.name)

    # Print all tracks in album
    for i in album_serialized.data[0].relationships.tracks.data:
        msg = (
            f"{i.id} | {i.attributes.album_name} | {i.attributes.artist_name} [{i.attributes.name}]"
        )
        print(msg)

async def about_artist_te(artist_id):
    shazam = Shazam(language="ES")

    about_artist = await shazam.artist_about(
        artist_id,
        query=ArtistQuery(
            views=[
                ArtistView.FULL_ALBUMS,
                ArtistView.FEATURED_ALBUMS,
                ArtistView.LATEST_RELEASE,
                ArtistView.TOP_MUSIC_VIDEOS,
                ArtistView.SIMILAR_ARTISTS,
            ],
            extend=[
                ArtistExtend.ARTIST_BIO,
                ArtistExtend.BORN_OR_FORMED,
                ArtistExtend.EDITORIAL_ARTWORK,
                ArtistExtend.ORIGIN,
            ],
        ),
    )
    serialized = Serialize.artist_v2(about_artist)
    pprint(serialized)

def recognize_song_from_command_line():
    parser = argparse.ArgumentParser(description='Recognize song using Shazam.')
    parser.add_argument('file', type=str, help='Path to the audio file')
    args = parser.parse_args()
    
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(recognize_song_te(args.file))

def search_album_from_command_line():
    parser = argparse.ArgumentParser(description='Search for an album on Shazam.')
    parser.add_argument('album_id', type=int, help='Shazam album ID')
    args = parser.parse_args()

    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(search_album_te(args.album_id))

def recognize_and_search_from_command_line():
    parser = argparse.ArgumentParser(description='Recognize a song and search for its album on Shazam.')
    parser.add_argument('file', type=str, help='Path to the audio file')
    args = parser.parse_args()

    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(recognize_and_search_te(args.file))

def artist_info_from_command_line():
    parser = argparse.ArgumentParser(description='Get information about an artist from Shazam.')
    parser.add_argument('artist_id', type=int, help='Shazam artist ID')
    args = parser.parse_args()

    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.run_until_complete(about_artist_te(args.artist_id))

if __name__ == "__main__":
    recognize_song_from_command_line()
    search_album_from_command_line()
    recognize_and_search_from_command_line()
    artist_info_from_command_line()
