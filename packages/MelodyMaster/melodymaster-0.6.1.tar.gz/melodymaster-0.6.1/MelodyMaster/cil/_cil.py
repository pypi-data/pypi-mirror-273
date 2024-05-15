import argparse
import asyncio
import sys
from MelodyMaster import (
    recognize_song_te,
    about_artist_te,
    recognize_and_search_te,
    search_album_te,
    get_default_lyrics,
    get_alternative_lyrics,
    recognize_text
)

def print_help():
    print("Usage:")
    print("  {} <command>".format(sys.argv[0]))
    print("Commands:")
    print("  recognize_song : Recognize a track")
    print("  about_artist : Get artist information")
    print("  recognize_and_search : Recognize and search for a name track")
    print("  search_album : Search for an album by ID")
    print("  get_default_lyrics : Get default lyrics for a song")
    print("  get_alternative_lyrics : Get alternative lyrics for a song")
    print("  help : Show this help message")

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('command', choices=[
        'recognize_song',
        'artist_info_te',
        'recognize_and_search',
        'search_album',
        'get_default_lyrics',
        'get_alternative_lyrics',
        'recognize_text'
        'help'
    ])
    parser.add_argument('--title', type=str, help='Song title or title and artist')
    parser.add_argument('--str', type=str, help='Whether to treat the input as a string or not')
    parser.add_argument('--duration', type=str, help='Song duration')
    parser.add_argument('--artist', type=str, help='Song artist')
    parser.add_argument('--file_path', type=str, help='Path to audio file')
    parser.add_argument('--album_id', type=int, help='Album id')
    parser.add_argument('--lang', type=int, help='lang')

    args = parser.parse_args()

    if args.command == 'help':
        print_help()
        return

    if args.command == 'get_default_lyrics':
        if args.title is None:
            print("Error: Missing song title.")
            print_help()
            return

        asyncio.run(get_default_lyrics(args.title, args.str or "true"))
        return

    if args.command == 'get_alternative_lyrics':
        if args.title is None:
            print("Error: Missing song title.")
            print_help()
            return

        asyncio.run(get_alternative_lyrics(args.title, args.artist or "", args.duration or "", args.str or "true"))
        return

    if args.command == 'recognize_text':
        if args.file_path is None:
            print("Error: Missing audio file_path.")
            print_help()
            return
        if args.lang is None:
            print("Error: Missing audio lang.")
            print_help()
            return

        asyncio.run(recognize_text(args.file_path, args.lang))
        return

    if args.command == 'recognize_song':
        asyncio.run(recognize_song_te(args.file_path))
    elif args.command == 'about_artist':
        asyncio.run(about_artist_te(args.title))
    elif args.command == 'recognize_and_search':
        asyncio.run(recognize_and_search_te(args.file_path))
    elif args.command == 'search_album':
        asyncio.run(search_album_te(args.album_id))
    else:
        print("Unknown command:", args.command)
        print_help()

if __name__ == "__main__":
    main()
    