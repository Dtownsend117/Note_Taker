import speech_recognition as sr
from datetime import datetime
import os

class Notes:
    def __init__(self, filename='notes.txt'):
        self.filename = filename
        self.recognizer = sr.Recognizer()
        self.last_date = None  # Keep a record of the dates of the notes

        # Phrases to trigger the options
        self.phrases = {
            'show_notes': ['one', 'display', 'display notes', 'list', 'show', 'show notes', 'display notes', 'list notes'], # Phrases to show notes on the screen
            'add_notes': ['two', 'add' 'add notes', 'take a note', 'record a note'], #Phrases to add notes to the file
            'new_notes_page': ['three', 'new page', 'create new page', 'new notes page', 'create new notes page', 'start new notes page'], #Phrases to create a new notes txt file
            'exit': ['four', 'exit', 'quit', 'close', 'never mind', 'scratch that'] # Phrases to exit the module
        }

    def take_note(self):
        print("Please speak your note...")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            note = self.recognizer.recognize_google(audio)
            print(f"You said: {note}")
            self.save_note(note)
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    def save_note(self, note):
        current_date = datetime.now().strftime("%Y-%m-%d")
        timestamp = datetime.now().strftime("%H:%M:%S")

        with open(self.filename, 'a') as file:
            if self.last_date != current_date:
                if self.last_date is not None:
                    file.write("\n")
                file.write(f"{current_date}\n") # Autofills the date in the txt file
                file.write("============================\n") # Note separator 
                self.last_date = current_date

            file.write(f"({timestamp}) {note}\n")
        print("Note saved.")

    def show_notes(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                notes = file.read()
                print("\n--- Notes ---")
                print(notes)
                print("--------------\n")
        else:
            print("No notes found.")

    def ask_to_continue(self): # Asks if you would like to add a new note
        print("Do you want to add another note? Please say 'yes' or 'no'.")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            response = self.recognizer.recognize_google(audio)
            print(f"You said: {response}")
            return response.lower() in ['yes', 'y']
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return False
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return False

    def new_notes_page(self):
        new_filename = input("Enter the new filename (without extension): ") + '.txt'
        self.filename = new_filename
        self.last_date = None
        print(f"New notes page created: {self.filename}")

    def display_menu(self):
        print("\n--- Note Taking Menu ---")
        print("1. Show Notes")
      # print (add something here if you would like a larger space between options) # repeat between the others
        print("2. Add Notes")
        print("3. New Notes Page")
        print("4. Exit")
        print("------------------------")

    def verbal_menu_selection(self):
        print("Please say your choice.")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            choice = self.recognizer.recognize_google(audio)
            print(f"You said: {choice}")
            return choice.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

    def is_valid_choice(self, choice):
        for action, phrases in self.phrases.items():
            if any(phrase in choice for phrase in phrases):
                return action
        return None

if __name__ == "__main__":
    notes = Notes()
    
    while True:
        notes.display_menu()
        choice = notes.verbal_menu_selection()

        if choice is not None:
            action = notes.is_valid_choice(choice)

            if action == 'show_notes':
                notes.show_notes()
            elif action == 'add_notes':
                notes.take_note()
                if not notes.ask_to_continue():
                    print("Exiting the note-taking application.")
                    break
            elif action == 'new_notes_page':
                notes.new_notes_page()
            elif action == 'exit':
                print("Exiting the note-taking application.")
                break
            else:
                print("Invalid choice. Please select a valid option.")
