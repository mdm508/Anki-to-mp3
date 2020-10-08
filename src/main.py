"""
main.py
10/7 Matthew McLaughlin

The goal is to create an album of mp3s that can be used
for language learning. In the current use case 
I have a bunch of audio that I got from anki cards
and I want to make a large album out of it. The audio clips
are relatively short. The goal is to merge the short audio
clips together splicing in short pauses to practice speaking.

Various options dictate how the merged track sound. For example,
we can add longer pauses between tracks to give the speaker
time to say the audio clip they just heard
"""
from autil import *
## Below are a bunch of options 
# Mp3s are written to this directory
# This folder must exist
OUT_PATH = "../output"
# How many times a clip is repeated
# Example, mp3 audio is "Hello", repeat is 1 then
# you repeat "Hello" clip 1 time
REPEAT = 1
# In seconds, how long of a pause should be added betwen clips?
# Note that this number of seconds will be LENGTH_OF_TRACK + ADDED_PAUSE
# So, if the track "Hello there" takes 2 seconds two play and ADDED_PAUSE is 3
# the total track length is 5 seconds
ADDED_PAUSE = 2.5
# How many minutes should a track be?
# This is really innacurate cause of ffmpeg problem with
# metadata. for me i have found take half of what you actually want
# for MAX_MIN
MAX_MINUTES = 10 #probably will do 20 min track
MAX_SECONDS = MAX_MINUTES * 60
# Leave as true if tracks should be broken into different albums
PUT_TRACKS_INTO_ALBUMS = True
# What is the maximum total length in minutes of an album?
MAX_ALBUM_MINUTES = 100
MAX_ALBUM_SECONDS = MAX_ALBUM_MINUTES * 60
# What should tag be for artist and album?
ARTIST="MY"
# Album will have format ALBUM_PREFIX + #album num
ALBUM_PREFIX = ARTIST

def main():
    print("Started")
    mp3_paths = list(make_mp3_paths())
    cur = create_empty_audio() 
    track_num, album_num = 1, 1
    album_seconds = 0 # how many seconds in cur album
    for loop_num, p in enumerate(mp3_paths, start=1):
        if should_print_report(loop_num, 50):
            print_progress_report(loop_num, len(mp3_paths))
        cur += make_audio_repition(path_to_mp3=p,
                                   pause_time=ADDED_PAUSE,
                                   repeat=REPEAT)
        if cur.duration_seconds > MAX_SECONDS:
            # export current track
            out_path = make_output_path(track_num, OUT_PATH)
            cur.export(out_path, format="mp3")
            print(f"wrote {out_path}")
            # tag current track
            update_tag(out_path, ARTIST, f"{ALBUM_PREFIX} {album_num}")
            # prepare for next track
            album_seconds += cur.duration_seconds
            if album_seconds > MAX_ALBUM_SECONDS:
                album_num += 1
                album_seconds = 0
            cur = create_empty_audio()
            track_num += 1
    print("Done")

if __name__ == "__main__":
    main()
