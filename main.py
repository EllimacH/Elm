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
                case default:
                    return reply_keyword[key]
    return "Sorry, I cannot understand."


def main():
    text_output = pyttsx3.init()
    mic = pyaudio.PyAudio()
    ready_to_talk = False

    stream = mic.open(format=pyaudio.paInt16, channels=1,
                      rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()

    while True:
        data = stream.read(4000)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()[14:-3]
            if result != "":
                try:
                    result = recognizer.Result()[14:-3]
                    if "hello" in result and not ready_to_talk:
                        ready_to_talk = True
                        msg = "Hello user, how can I help you?"
                        print(f"Elm: {msg}")
                        text_output.say(msg)
                        text_output.runAndWait()
                    elif result == "goodbye" and ready_to_talk:
                        msg = "Goodbye user"
                        print(f"Elm: {msg}")
                        text_output.say(msg)
                        ready_to_talk = False
                        text_output.runAndWait()
                    elif ready_to_talk:
                        print(result)
                        reply = checkMatch(result)
                        print("Elm: " + reply)
                        text_output.say(reply)
                        text_output.runAndWait()
                except:
                    pass


if __name__ == '__main__':
    main()
