"""
autil.py are audio utility functions
Matthew McLaughlin
"""
from re import compile, search
from os.path import join as path_join
from os.path import exists
from pydub import AudioSegment
from sys import exit
import eyed3
import warnings

# folder where input resources are located
RES = "../res"
# This folder must hold the mp3s
MP3_RELPATH = path_join(RES, "mp3s") 
# Name of txt file containing the path names for each mp3
# The mp3s will be output in the same order in this file
MP3_FILENAMES = path_join(RES, "names.txt")
# How many loops before printing the progress reports
PROGRESS_REPORT_FREQ = 20
# How many progress stars should show up in command line
STARS = 10
"""
A collection of utility functions to be
used by the main program.
"""

# Constructing the path
# These functions are useful in the case
# You are taking the mp3 files from an anki
# collection and you want to maintain there order
def parse_anki_filename(name:str):
    """
    Remove non filename components from filename
    """
    pattern = compile(r"(sound:)(.*mp3)")
    return search(pattern, name).group(2)


def make_path(filename:str):
    """
    given filename construct a path to the 
    that filename. Assume that the file lives in
    ../res/mp3s.
    If it is a valid path returns the path otherwise
    returns False so that later this path can be filtered out.
    """
    path = path_join(MP3_RELPATH, filename)
    return path 

def make_audio_repition(path_to_mp3:str, pause_time=0, repeat=0):
    """
    make an mp3 from the given path so that this mp3 when played
    has the following structure

    (mp3 + pause_time) x repeat

    which means the track would play its audio, pause for pause_time
    seconds and then repeat this pattern repeat times
    """
    sound_clip = AudioSegment.from_mp3(path_to_mp3)
    silence = AudioSegment.silent(duration=1000*pause_time)
    sound = sound_clip + silence
    for _ in range(repeat):
        sound += sound_clip + silence
    return sound

def update_tag(path_to_mp3:str, artist="someone", album="some album"):
    """
    remove any pre-exiting tags from the input mp3
    and updates tags using artist and album
    """
    audio = eyed3.load(path_to_mp3)
    audio.initTag()
    audio.tag.artist = artist
    audio.tag.album = album
    audio.tag.save()

def make_mp3_paths(mp3_filenames=MP3_FILENAMES):
    """
    returns iterator of only the valid mp3 paths
    """
    with open(mp3_filenames) as f:
        try:
            return filter(lambda path: exists(path), 
                            map(make_path, 
                            map(parse_anki_filename, f.readlines()))) 
        except:
            print("exception occured when attempting to create \
            the mp3 path names")
            print("exiting")
            exit()

def make_output_path(track_num, base_dir):
    """
    use track_num to give a name to the track.
    return the path to export the mp3 to
    """
    return path_join(base_dir, str(track_num)) + ".mp3"

def should_print_report(loop_number, freq=PROGRESS_REPORT_FREQ):
    return loop_number % freq  == 0

def print_progress_report(loop_number, total_loops):
    p = int(round(loop_number / total_loops, 2) * STARS)
    print(f"{p * '*'}{(STARS-p) * '-'}")

def create_empty_audio():
    return AudioSegment.silent(duration=0)
