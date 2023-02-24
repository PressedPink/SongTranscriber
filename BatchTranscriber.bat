@echo off

set env_path = .\env
set venv_path = .\venv


set /p playlist_link="Enter the URL of the YouTube playlist: "

py -m yt-dlp -x --embed-thumbnail --audio-format mp3 -o "%(title)s.%(ext)s" "%playlist_link%"

call %env_path%\Scripts\activate.bat

python .\Splitter.py

call %env_path%\Scripts\deactivate.bat

call %venv_path%\Scripts\activate.bat

python .\Transcriber.py

call %venv_path%\Scripts\deactivate.bat