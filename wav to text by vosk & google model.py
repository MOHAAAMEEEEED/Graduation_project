

import os
import wave
import json
import vosk
import subprocess
from pydub import AudioSegment
import speech_recognition as sr

# Function to extract audio from a video file
def extract_audio(video_file, output_audio_file):
    # FFmpeg command to extract audio
    command = ['ffmpeg', '-i', video_file, '-q:a', '0', '-map', 'a', output_audio_file]
    # Run the command
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Function to convert audio to WAV format with correct properties
def convert_to_wav(audio_file, output_file):
    # Load audio using pydub
    audio = AudioSegment.from_file(audio_file)
    
    # Convert to mono (1 channel) if necessary
    if audio.channels > 1:
        audio = audio.set_channels(1)
    
    # Set the sample width to 2 bytes (16-bit PCM)
    audio = audio.set_sample_width(2)
    
    # Ensure the sample rate is something Vosk can handle (16000 is common)
    audio = audio.set_frame_rate(16000)
    
    # Export to WAV in PCM format
    audio.export(output_file, format="wav")
    return output_file

"""# Function to transcribe WAV audio using Google Speech Recognition
def transcribe_with_google(wav_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)
    return text"""

# Function to transcribe WAV audio using Vosk
def transcribe_with_vosk(model_path, wav_file):
    if not os.path.exists(model_path):
        print(f"Model at {model_path} not found.")
        return
    
    model = vosk.Model(model_path)
    wf = wave.open(wav_file, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 44100, 48000]:
        print("Audio file must be WAV format mono PCM.")
        return

    recognizer = vosk.KaldiRecognizer(model, wf.getframerate())
    recognizer.SetWords(True)

    result = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            part_result = json.loads(recognizer.Result())
            result += part_result.get("text", "") + " "

    wf.close()
    final_result = json.loads(recognizer.FinalResult())
    result += final_result.get("text", "")

    return result

# Main function to handle extraction, conversion, and transcription
def main(video_file, model_path):
    # Extract audio from video file
    output_audio_mp3 = "output_audio.mp3"
    output_audio_wav = "output_audio.wav"
    extract_audio(video_file, output_audio_mp3)

    # Convert MP3 to WAV for speech recognition
    convert_to_wav(output_audio_mp3, output_audio_wav)

    """# Transcribe using Google Speech Recognition
    try:
        google_transcription = transcribe_with_google(output_audio_wav)
        print("Google Transcription:", google_transcription)
    except Exception as e:
        print(f"Google Speech Recognition failed: {e}")"""

    # Transcribe using Vosk
    try:
        vosk_transcription = transcribe_with_vosk(model_path, output_audio_wav)
        print("Vosk Transcription:", vosk_transcription)
    except Exception as e:
        print(f"Vosk Speech Recognition failed: {e}")

# Example usage
video_file = "F:/Seventh Term/graduation project/test/New folder/English Story For Listening - Practice English Speaking with Stories.mp4"
model_path = "F:/Seventh Term/graduation project/test/New folder/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"  # Replace with the path to your Vosk model

main(video_file, model_path)
