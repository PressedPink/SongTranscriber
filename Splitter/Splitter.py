import subprocess
import glob
import os
import multiprocessing
from pathlib import Path
from multiprocessing import Pool, Process, Value, Semaphore
import sys
import socket
import socketserver
from threading import BoundedSemaphore
import time



def alertTranscriber(globSize):
    os.makedirs(os.path.dirname('./output/'), exist_ok=True)
    while(True):
        songs = glob.glob('./output/*')
        print(songs)
        if(globSize == len(songs)):
            break
        else:
            time.sleep(1)

    HOST, PORT = "localhost", 10000
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(str(globSize), "utf-8"))
        received = str(sock.recv(1024), "utf-8")


def spleeterCall(song):
    #subprocess.call(f"py -m spleeter separate -p spleeter:2stems -o output {song}", shell=True)
    pass

def releaseSema(val):
    val.release()

def stripAndSplit(pool_sema):
    songs = glob.glob('../Server/input/*.mp3')

    poolSize = 0
    if(len(songs) <= 10):
        poolSize = len(songs)
    else:
        poolSize = 10
    
    pool = multiprocessing.Pool(processes=poolSize)

    new_song_names = []
    for song in songs:
        new_name = song.replace("&", "_")
        new_name = new_name.replace(" ", "_")
        os.rename(song, new_name)
        new_song_names.append(new_name)

    return pool.map_async(spleeterCall, new_song_names), len(songs)

if __name__ == '__main__':

    multiprocessing.set_start_method('spawn')
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 9999  # Port to listen on (non-privileged ports are > 1023)

    pool_sema = None

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while(True):
            conn, addr = s.accept()
            with conn:
                conn.sendall(bytes(" ", "utf-8"))
                pool, pool_sema = stripAndSplit(pool_sema)
                Process(target = alertTranscriber, args=(pool_sema, )).start()