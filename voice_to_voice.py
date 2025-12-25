import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
import pyttsx3


# load the safe
load_dotenv()

# openai
client = OpenAI()

# The Ears
def listen():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening....(Speak Now)")

            # Adjustt ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            # Listen for audio input
            audio = recognizer.listen(source,timeout=5,phrase_time_limit=10)
            print("processing")

        # Recognize speech using Google's Free API
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    
    except sr.WaitTimeoutError:
        msg = "No speech detected (timeout)."
        speak(msg)
        return None
    except sr.UnknownValueError:
        msg = "Sorry, I did not catch that."
        speak(msg)
        return None
    except sr.RequestError:
        msg = "Speech recongnition service unavailable."
        speak(msg)
        return None
    except Exception as e:
        print(f"An error occured in listen(): {e}")
        return None
    
# The thinking part
def think(text: str)-> str:
    if not text:
        return None
    print("Thinking....")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages= [
                {"role":"user","content":text}
            ],
        )
        response_text = response.choices[0].message.content
        print(f"AI said: {response_text}")
        return response_text
    
    except Exception as e:
        print(f"An error occured in think(): {e}")
        return "Sorry, something went wrong while thinking"
    

# The mouth
def speak(text: str) -> str:
    if not text:
        return 
    
    try:
        engine = pyttsx3.init()
        # changing voices
        voices = engine.getProperty("voices")
        if voices:
            # Index 0 -> 1 for alternate voice
            engine.setProperty("voice", voices[1].id)

        engine.setProperty("rate", 175) #Speed of voice

        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print(f"An error occured on speak(): {e}")
    
def main():
    print("------Voice Assistant Started------")
    speak("Hello, I am ready. You can start speaking... I was created by Barron")


    while True:
        # Listen
        user_input = listen()

        # skip if nothing heard
        if not user_input:
            continue

        # check for exit keywords
        if user_input.lower().strip() in ["exit","stop","quit"]:
            speak("Goodbye!")
            print("Exiting....")
            break

        # think
        ai_response = think(user_input)

        # speak
        speak(ai_response)


if __name__ == "__main__":
    main()