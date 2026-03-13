@echo off
echo Starting NLP TTS Application...

cd /d "%~dp0"

start http://localhost:8501
streamlit run app.py

pause