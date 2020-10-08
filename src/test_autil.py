"""
Tests for autil.py
listed in no particular order 
"""
from autil import *
import pytest


def test_make_output_path():
    base_dir = "../output"
    for i in range(1000):
        assert make_output_path(i, base_dir) == path_join(base_dir, str(i))  + ".mp3"
            
def test_parse_anki_filename():
    data = [
            ("[sound:tmp1cctcn.mp3]", "tmp1cctcn.mp3"),
            ("[sound:333158.mp3]", "333158.mp3"),
            ("[sound:tmpsxkriw.mp3]", "tmpsxkriw.mp3"),
            ("[sound:tmp4tzxbu.mp3]", "tmp4tzxbu.mp3"),
            ("[sound:tmpxth4o3.mp3]", "tmpxth4o3.mp3"),
            ("[sound:333012.mp3]", "333012.mp3")
            ]
    for filename, expected in data:
        assert parse_anki_filename(filename) == expected

def test_make_path():
    data = ["f1.mp3",
            "f2.mp3",
            "f3.mp3"
            ]
    for filename in data:
        expected = path_join("../res/mp3s", filename)
        assert expected == make_path(filename)



def test_update_tag():
    warnings.filterwarnings("ignore")
    update_tag("testres/short.mp3")
    audio = eyed3.load("testres/short.mp3")
    assert audio.tag.artist == "someone"
    assert audio.tag.album == "some album"


@pytest.mark.skip(reason="only to discover nice length")
def test_make_audio_repition():
    for name in ['short','medium','long']:
        for p_time in range(1,10):
            audio = make_audio_repition(
                    f"testres/{name}.mp3",
                    p_time,
                    1)
            audio.export(
                    f"testres/out/{name}_pause{p_time}.out.mp3",
                    format="mp3")





