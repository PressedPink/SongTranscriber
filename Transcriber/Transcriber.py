import whisper
import glob
import os
import multiprocessing
from pathlib import Path
from multiprocessing import Pool, Process
import openai
import socket
import sys
import time

api_key = os.environ.get('OPENAI_API_KEY')

openai.api_key = api_key


def transcribe(song):
    model = whisper.load_model("small.en")

    model_engine = "text-davinci-003"

    songPrompt = "Can you format this text like lyrics? Try to split into verses and choruses, where a chorus is lines that get repeated."
    
    result = model.transcribe(song)
    formattedTranscribe = ""

    
    for word in str(result["text"]).split(" "):
        if(len(word) == 0): continue
        else: formattedTranscribe += word + " "

    songPrompt = songPrompt + formattedTranscribe
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=songPrompt,
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5
     )
    response = completion.choices[0].text
    os.makedirs(os.path.dirname('./TextOutput/'), exist_ok=True)
    f = open(f"./TextOutput/{Path(song).parts[-2]}.txt", "w")
    f.write(response)
    f.close()

def returnToServer(globSize):
    while(True):
        os.makedirs(os.path.dirname('./TextOutput/'), exist_ok=True)
        songs = glob.glob('./TextOutput/*')
        print(songs)
        if(globSize == len(songs)):
            break
        else:
            time.sleep(1)


if __name__ == '__main__':
    HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
    PORT = 10000  # Port to listen on (non-privileged ports are > 1023)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while(True):
            conn, addr = s.accept()
            with conn:
                globSize = int(conn.recv(sys.getsizeof(24)))
                conn.sendall(bytes(" ", "utf-8"))
                new_song_names = glob.glob('../Splitter/output/**/vocals.wav')
                print(new_song_names)
                pool = multiprocessing.Pool(processes=10)
                r = pool.map_async(transcribe, new_song_names)
                Process(target=returnToServer, args=(globSize, )).start()
                
