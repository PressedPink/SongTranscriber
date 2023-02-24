set current_dir=%cd%

start /w /b wt -d %current_dir% pwsh -NoExit -c ".\env\Scripts\activate && python ./Splitter.py"

start /w /b wt -d %current_dir% pwsh -NoExit -c ".\venv\Scripts\activate && python ./Transcriber.py"