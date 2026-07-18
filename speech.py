import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()

    recognizer.pause_threshold = 3.0
    recognizer.non_speaking_duration = 1.0
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        print("Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(
            source,
            timeout=None   # Wait indefinitely until speech starts
        )

    try:
        text = recognizer.recognize_google(audio)
        return text

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        return "Google Speech Recognition service unavailable."