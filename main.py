from vosk import Model, KaldiRecognizer
import pyaudio
import os
import json
import pyttsx3
from datetime import date, datetime

MODEL = Model(os.path.join(os.path.dirname(__file__),
              "vosk-model-small-en-us-0.15").replace("\\", "/"))
recognizer = KaldiRecognizer(MODEL, 16000)

reply_keyword = {}
with open("reply_keyword.json", "r") as f:
    reply_keyword = json.load(f)


def checkMatch(sentence: str) -> str:
    for key in reply_keyword:
        if key in sentence:
            match reply_keyword[key]:
                case "GET_DATE":
                    return date.today().strftime("%B %d, %Y")
                case "GET_TIME":
                    return datetime.now().strftime("%H:%M:%S")
    return "Sorry, I cannot understand."

def botSpeak(text, inputSource, outputSource):
    # halt the input source
    inputSource.stop_stream()
    # speak the text
    outputSource.say(text)
    outputSource.runAndWait()
    # resume the input source
    inputSource.start_stream()

def main() -> None:
    text_output = pyttsx3.init()
    mic = pyaudio.PyAudio()
    ready_to_talk = False

    voice_input = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    voice_input.start_stream()

    # Clear the terminal
    os.system("cls") if os.name == "nt" else os.system("clear")

    while True:
        data = voice_input.read(4000, exception_on_overflow = False)
        result = ""
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()[14:-3]
        if result == "":
            continue
        if result == "goodbye" and ready_to_talk:
            msg = "Goodbye user"
            print(f"Elm: {msg}")
            botSpeak(msg, voice_input, text_output)
            ready_to_talk = False
        elif result == "hello" and not ready_to_talk:
            ready_to_talk = True
            msg = "Hello user, how can I help you?"
            print(f"Elm: {msg}")
            botSpeak(msg, voice_input, text_output)
        elif ready_to_talk:
            print("You: " + result)
            reply = checkMatch(result)
            print("Elm: " + reply)
            botSpeak(reply, voice_input, text_output)

if __name__ == '__main__':
    main()
