import numpy as np
import random
import re
import json
import pyttsx3
import speech_recognition as sr
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob

class Bot:
    def __init__(self, name, jsonfile):
        self.name = name
        self.conversations = self.load_conversations(jsonfile)
        self.engine = pyttsx3.init()

    def preprocess_text(self, text):
        # Correct spelling mistakes using TextBlob
        corrected_text = str(TextBlob(text).correct())

        # Tokenization
        tokens = word_tokenize(corrected_text)

        # Stopword removal and remove non-alphabetic characters
        stop_words = set(stopwords.words('english'))
        tokens = [re.sub(r'[^a-zA-Z]', '', token).lower() for token in tokens if token.lower() not in stop_words]

        # Remove empty tokens
        tokens = [token for token in tokens if token]

        return tokens

    def generate_response(self, user_input):
        max_similarity = 0
        best_response = None
        try:
            for entry in self.conversations:
                question = entry["question"]
                question_tokens = self.preprocess_text(question)
                user_input_tokens = self.preprocess_text(user_input)
                common_tokens = set(question_tokens) & set(user_input_tokens)
            
                # Check for division by zero
                if len(question_tokens) == 0 or len(user_input_tokens) == 0:
                    similarity = 0
                else:
                    similarity = len(common_tokens) / max(len(question_tokens), len(user_input_tokens))

                if similarity > max_similarity:
                    max_similarity = similarity
                    best_response = entry.get("answers", ["I'm sorry, I don't have a response for that."])

            if best_response:
                return random.choice(best_response)
            else:
                return "I'm sorry, I didn't understand your question."

        except BaseException as e:
            return f"Error: {e}"

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def load_conversations(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def run(self):
        while True:
            user_input = input("You: ")  # Wait for user to input command
            if user_input.lower() == '/m on':
                self.listen_for_input()  # Start listening for speech input
            elif user_input.lower() == 'exit':
                break
            else:
                bot_response = self.generate_response(user_input)
                print(f"{self.name}: {bot_response}")
                self.speak(bot_response)

    def listen_for_input(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust microphone for ambient noise
            audio = recognizer.listen(source)  # Listen for audio input

        try:
            print("Recognizing...")
            user_input = recognizer.recognize_google(audio)  # Recognize speech using Google Speech Recognition
            print("You:", user_input)  # Print "You: " before the recognized user input
            # Process the recognized user input here
            bot_response = self.generate_response(user_input)
            print(f"{self.name}: {bot_response}")
            self.speak(bot_response)
        except sr.UnknownValueError:
            print("JZ: Sorry, I could not understand your speech.")
        except sr.RequestError as e:
            print("JZ: Speech recognition request failed:", e)



