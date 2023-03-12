from multiprocessing import Process
from multiprocessing import Pool
import subprocess
from flask import Flask
from flask import request
import json
from flask import jsonify
import sys
from flask_cors import CORS
import socket
import time


def downAndOut(linkJson):
    #subprocess.call(f'yt-dlp -x --audio-format mp3 -P ./input -o "%(title)s.%(ext)s" "{linkJson["link"]}"', shell=True)
    HOST, PORT = "localhost", 9999
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(" ", "utf-8"))
        received = str(sock.recv(1024), "utf-8")
    
if __name__ == '__main__':
    

    r = None
    app = Flask(__name__)
    CORS(app)

    @app.route("/SongTranscriber", methods=['POST'])
    def SongTranscriber():
        linkJson = request.get_json()
        resp = jsonify(success=True)
        Process(target=downAndOut, args=(linkJson,)).start()

        return resp
        #json.dumps(linkJson)
    #Function for song transcriber
    #POST request


    @app.route("/Status", methods=['GET'])
    def constantQuery():
        pass
    #Function for status
        try:
            r.successful()
        except:
            #return what has been split so far
            pass
        else:
            #everything that has been split and the fact that there are no more things being split
            #Send tcp request to transcriber
            pass
    app.run(port=5000, debug=True)