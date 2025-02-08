
import json
import random
import os
import subprocess
import argparse

# ANSI escape codes for colors
GREEN = '\033[92m'
RESET = '\033[0m'

def load_words(file_path="speech-demo.json"):
    """Loads words from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{file_path}'.")
        return []

def choose_word(words, used_words):
    """Chooses a random word that has not been used yet."""
    available_words = [word for word in words if word['en'] not in used_words]
    if not available_words:
        print("All words have already been used!")
        return None
    return random.choice(available_words)

def generate_options(correct_word, language):
    """Generates jumbled options based on the correct word."""
    key_to_use = 'en' if language == 'en' else 'ua'
    correct_sentence = correct_word[key_to_use]
    words = correct_sentence.split()
    random.shuffle(words)
    return " ".join(words)

def speak_word(word):
    """Speaks the word in English (uses `say` on macOS or `espeak` on Linux)."""
    try:
        if os.name == 'posix':  # Linux or macOS
            try:
                subprocess.run(['say', word], check=True, capture_output=True)  # macOS
            except FileNotFoundError:
                try:
                    subprocess.run(['espeak', word], check=True, capture_output=True)  # Linux
                except FileNotFoundError:
                    print("The 'say' (macOS) or 'espeak' (Linux) program for speech synthesis was not found.")
        elif os.name == 'nt':  # Windows (requires installed TTS, e.g., pyttsx3)
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say(word)
                engine.runAndWait()
            except ImportError:
                print("The 'pyttsx3' module for speech synthesis is not installed. Install it: pip install pyttsx3")
            except Exception as e:
                print(f"Error during speech synthesis on Windows: {e}")
        else:
            print("Speech synthesis is not supported on this operating system.")
    except subprocess.CalledProcessError as e:
        print(f"Error during speech synthesis: {e}")

def clear_terminal():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def is_answer_correct(user_input, correct_answer_en, correct_answer_ua, language):
    """Checks if the user's answer is correct."""
    correct_answer = correct_answer_en if language == 'en' else correct_answer_ua
    return user_input.lower() == correct_answer.lower()


def main():
    """The main game logic."""
    parser = argparse.ArgumentParser(description="Game for learning words.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--lang-ua", action="store_true", help="Display Ukrainian words.")
    group.add_argument("--lang-en", action="store_true", help="Display English words.")
    parser.add_argument("--data", default="speech-demo.json", help="Path to the JSON file with data.")

    args = parser.parse_args()

    language = 'en' # Default to 'en' if no argument is specified
    if args.lang_ua:
      language = 'ua'

    words = load_words(args.data)
    if not words:
        return

    used_words = set()  # Set to store already used words
    correct_count = 0
    incorrect_count = 0

    print("Enter 's' to speak the word, 'q' to quit the game.")

    while True:
        word = choose_word(words, used_words)
        if not word:
            print("You win! All words have been learned.")
            break  # Exit the loop if all words have been used

        # Determine the correct time and format the time options string
        time_value = word.get('times', 'Unknown')  # Get the 'times' value, or 'Unknown' if it doesn't exist
        type_value = word.get('type', 'Unknown')

        #Highlighting
        past_color = ""
        present_color = ""
        future_color = ""
        affirmation_color = ""
        question_color = ""
        negation_color = ""

        if time_value.lower() == "past":
          past_color = GREEN
        elif time_value.lower() == "present":
          present_color = GREEN
        elif time_value.lower() == "future":
          future_color = GREEN

        if type_value.lower() == "affirmation":
            affirmation_color = GREEN
        elif type_value.lower() == "question":
            question_color = GREEN
        elif type_value.lower() == "negation":
            negation_color = GREEN

        time_options = f"{past_color}Past{RESET}      {present_color}Present{RESET}      {future_color}Future{RESET}"
        types_options = f"{question_color}Question{RESET}  {affirmation_color}Affirmation{RESET}  {negation_color}Negation{RESET}"

        print(time_options)
        print(types_options)

        question_translation = word['ua'] if language == 'en' else word['en']  # What language to ask in
        jumbled_sentence = generate_options(word, language)

        #print(f"\nTranslation: {question_translation}")
        print(f"\n{question_translation}")
        #print("Rearrange the words to form the correct sentence:")
        print(f"{jumbled_sentence}")


        while True:
            #user_input = input("Your answer: ").lower()
            user_input = input("> ").lower()
            correct_answer_en = word['en'].lower()  # Correct answer (eng) in lowercase
            correct_answer_ua = word['ua'].lower()  # Correct answer (ukr) in lowercase

            if user_input == 'q':
                print("Game over!")
                if correct_count > 0 or incorrect_count > 0:
                    print(f"Correct answers: {correct_count}")
                    print(f"Incorrect answers: {incorrect_count}")
                return

            if user_input == 's':
                speak_word(word['en'])
            elif is_answer_correct(user_input, correct_answer_en, correct_answer_ua, language):
                print(f"{GREEN}Correct!{RESET}")  # Print "Correct!" in green
                speak_word(word['en'])
                used_words.add(word['en'])
                correct_count += 1
                clear_terminal()  # Clear the terminal
                break
            else:
                print("Incorrect. Try again.")
                incorrect_count += 1


    if correct_count > 0 or incorrect_count > 0:
        print(f"Correct answers: {correct_count}")
        print(f"Incorrect answers: {incorrect_count}")


if __name__ == "__main__":
    main()
