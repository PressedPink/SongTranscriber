import subprocess
import numpy as np
import glob
import os
import multiprocessing
from pathlib import Path
from multiprocessing import Pool


def spleeterCall(song):
    subprocess.call(f"py -m spleeter separate -p spleeter:2stems -o output {song}", shell=True)

if __name__ == '__main__':

    songs = glob.glob('*.mp3')
    new_song_names = []
    for song in songs:
        new_name = song.replace(" ", "_")
        os.rename(song, new_name)
        new_song_names.append(new_name)


    pool = multiprocessing.Pool(processes=10)
    r = pool.map_async(spleeterCall, new_song_names)
    r.wait()
