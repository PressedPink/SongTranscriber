import whisper
import glob
import os
import multiprocessing
from pathlib import Path
from multiprocessing import Pool
import openai

api_key = os.environ.get('OPENAI_API_KEY')

openai.api_key = api_key


def transcribe(song):
    model = whisper.load_model("small.en")

    model_engine = "text-davinci-003"

    songPrompt = "Can you format this text like lyrics? Try to split into verses and choruses, where a chorus is lines that get repeated."
    
    result = model.transcribe(f"./output/{Path(song).stem}/vocals.wav")
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
    f = open(f"./TextOutput/{Path(song).stem}.txt", "w")
    f.write(response)
    f.close()

if __name__ == '__main__':

    new_song_names = glob.glob('./output/*.mp3')

    pool = multiprocessing.Pool(processes=10)
    r = pool.map_async(transcribe, new_song_names)
    r.wait()
