import json
import random
import os
import subprocess
import argparse

# ANSI escape codes for colors
GREEN = '\033[92m'
RESET = '\033[0m'

def load_words(file_path="data.json"):
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

def generate_options(correct_word, words, language, number_of_options=8):
    """Generates a list of answer options, including the correct one."""
    key_to_use = 'en' if language == 'en' else 'ua'
    correct_option = correct_word[key_to_use]
    options = [correct_option]

    # Remove correct word to not pick it as incorrect option
    available_words = [word for word in words if word[key_to_use] != correct_option]

    if len(available_words) < number_of_options - 1:
      print("Warning: Not enough unique words to generate all options.")
      num_incorrect_options = len(available_words)
    else:
      num_incorrect_options = number_of_options - 1

    try:  # Handle cases where available_words is empty.
        incorrect_options = random.sample(available_words, num_incorrect_options)
    except ValueError:
        incorrect_options = []

    options.extend([word[key_to_use] for word in incorrect_options])
    random.shuffle(options)
    return options

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

def is_answer_correct(user_input, correct_answer_en, correct_answer_ua, language, options):
    """Checks if the user's answer is correct."""
    if user_input in [str(i+1) for i in range(len(options))]:
        try:
            chosen_option = options[int(user_input)-1].lower()
            correct_answer = correct_answer_en if language == 'en' else correct_answer_ua
            return chosen_option == correct_answer
        except ValueError:
            return False # Invalid input, not a valid option number
    else:
        correct_answer = correct_answer_en if language == 'en' else correct_answer_ua
        return user_input == correct_answer


def main():
    """The main game logic."""
    parser = argparse.ArgumentParser(description="Game for learning words.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--lang-ua", action="store_true", help="Display Ukrainian words.")
    group.add_argument("--lang-en", action="store_true", help="Display English words.")
    parser.add_argument("--data", default="data.json", help="Path to the JSON file with data.")

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
            print("You win. All words have been learned.")
            break  # Exit the loop if all words have been used

        question_translation = word['ua'] if language == 'en' else word['en']  # What language to ask in
        options = generate_options(word, words, language)
        print(f"\nTranslation: {question_translation}")
        #print(f"{question_translation}")
        #print("Choose the correct option or enter the word:")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")

        while True:
            user_input = input("Your answer: ").lower()
            #user_input = input("> ").lower()
            correct_answer_en = word['en'].lower()  # Correct answer (eng) in lowercase
            correct_answer_ua = word['ua'].lower()  # Correct answer (ukr) in lowercase

            if user_input == 'q':
                print("Quitting the game.")
                if correct_count > 0 or incorrect_count > 0:
                    print(f"Correct answers: {correct_count}")
                    print(f"Incorrect answers: {incorrect_count}")
                return

            if user_input == 's':
                speak_word(word['en'])
            elif is_answer_correct(user_input, correct_answer_en, correct_answer_ua, language, options):
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
