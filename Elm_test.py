import speech_recognition as sr
import pyttsx3
from datetime import date, datetime
import json
import requests
import python_weather
import asyncio
import os
import pyaudio


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


def main() -> None:
    voice_input = sr.Recognizer()
    text_output = pyttsx3.init()

    ready_to_talk = False

    with sr.Microphone() as mic:
        audio = voice_input.listen(mic)
        while True:
            try:
                sentence = voice_input.recognize_google(audio)
                print(f"You: {sentence}")
                if "hello" in sentence and not ready_to_talk:
                    ready_to_talk = True
                    msg = "Hello user, how can I help you?"
                    print(f"Elm: {msg}")
                    text_output.say(msg)
                    text_output.runAndWait()
                elif sentence == "goodbye" and ready_to_talk:
                    msg = "Goodbye user"
                    print(f"Elm: {msg}")
                    text_output.say(msg)
                    ready_to_talk = False
                    text_output.runAndWait()
                elif ready_to_talk:
                    reply = checkMatch(sentence)
                    print("Elm: " + reply)
                    text_output.say(reply)
                    text_output.runAndWait()
            except:
                pass
            audio = voice_input.listen(mic)


if __name__ == "__main__":
    main()
