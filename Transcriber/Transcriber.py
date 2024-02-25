import whisper
import glob
import multiprocessing
import socket
import sys
from openai import OpenAI
import json


def transcribe(song):

    return ("COCK")

    #Load whisper model and build song transcription
    whisperModel = whisper.load_model("small.en")
    unformatedResult = whisperModel.transcribe(song)
    
    #Build prompt for GPT formatting
    modelDescription = "Format these song lyrics by labelling the verses and choruses of the song. Label verses with [Verse 1], [Verse 2], etc., and choruses with [Chorus]. Use the guideline that a chorus is a block of text typically consisting of multiple lines that is repeated throughout the song, and choruses occur between verses. Some songs don't have choruses. Do not add extra text, as this is an exact speech to text transcription of the audio. Just label the verses and choruses. Keep in mind that most verses are usually at least 8+ lines long. Try with this song: "
    songPrompt = modelDescription + unformatedResult["text"]

    #Create GPT client
    client = OpenAI()

    #Retrieve GPT response
    formatedResponse = client.chat.completions.create(
        model = "gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": songPrompt},
        ]
    )

    return formatedResponse.choices[0].message.content


if __name__ == '__main__':
    HOST = "127.0.0.1"
    PORT = 10000

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                globSize = int(conn.recv(sys.getsizeof(24)))
                conn.sendall(bytes(" ", "utf-8"))
                new_song_names = glob.glob('../Splitter/output/**/vocals.wav')
                
                # Use multiprocessing.Pool for both transcribing and monitoring
                with multiprocessing.Pool(processes=10) as pool:
                    transcriptions = pool.map(transcribe, new_song_names)
                    transcriptionsJson = bytes(json.dumps(transcriptions), encoding='utf-8')

                


                    

                
