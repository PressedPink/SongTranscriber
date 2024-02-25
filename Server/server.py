from multiprocessing import Process
import subprocess
from flask import Flask, request, jsonify
from flask_cors import CORS
import socket


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

        HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        PORT = 9998  # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                while True:
                    conn.sendall(bytes(" ", "utf-8"))
        return resp


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