import pyperclip
from pynput.keyboard import Key, Controller, Listener
import time
import threading

# Flag to choose between clipboard and a direct variable
USE_CLIPBOARD = True

# Global variables to control execution
running = True
simulating = False

DIVIDER_STRING = "/di"

# Delays between keystrokes
FAST_TYPING_DELAY = 0.022  # Ultra-fast delay for most keystrokes
DIVIDER_TYPING_DELAY = 0.6   # Slower delay for separators

# Ajoutez cette ligne pour définir un délai global
BEFORE_ENTER_DELAY = 0.15  # Délai avant d'appuyer sur la touche entrée
AFTER_ENTER_DELAY = 0.15

# Ajoutez ces lignes pour définir les variables globales
CHARACTER_PAUSE_LIMIT = 100  # Nombre de caractères après lesquels faire une pause
CHARACTER_PAUSE_DURATION = 0.6  # Durée de la pause en secondes

# Test text if not using the clipboard
TEST_TEXT = """# This Week
## Monday
- [ ] Team meeting at 9 AM
- [ ] Review quarterly report
- [ ] Lunch with a client
Here is a link: [test](http://test.com) 
---
## Tuesday
- [ ] Brainstorming session for the new project
- [ ] Update the KPI dashboard
- [ ] Yoga class at 6 PM
___
## Wednesday
*Wednesday tasks:*
- [ ] Work on the budget presentation
- [ ] Call with suppliers at 2 PM
- [ ] Buy a birthday gift for mom
---
## Thursday
*Thursday tasks:*
- [ ] Code review with the development team
- [ ] Prepare the agenda for Friday's meeting
- [ ] Dinner with friends
# Quote
> "Life is a mystery to be lived, and a mystery to be lived well."
> *Voltaire*
"""


def transform_text(text):
    # Replace "- [ ]" with "[]"
    text = text.replace("- [ ]", "[]")
    # Replace "---" or "___" with DIVIDER_STRING
    lines = text.splitlines()
    transformed_lines = []
    for line in lines:
        if line.strip() == "---" or line.strip() == "___":
            transformed_lines.append(DIVIDER_STRING)
        else:
            transformed_lines.append(line)
    return "\n".join(transformed_lines)

def get_text():
    if USE_CLIPBOARD:
        return transform_text(pyperclip.paste())
    else:
        return transform_text(TEST_TEXT)

def simulate_typing(text):
    global simulating
    keyboard = Controller()
    
    lines = text.splitlines()
    in_list = False  # To track if we are in a list
    char_count = 0  # Compteur de caractères tapés
    for i, line in enumerate(lines):
        if not simulating:
            print("Simulation interrupted.")
            break
        
        # Check if the line is part of a list
        is_list_item = line.lstrip().startswith(('-')) or (line.lstrip() and line.lstrip()[0].isdigit() and '.' in line.lstrip()[:3])
        is_task_item = line.lstrip().startswith("[]")
        
        # Simulate typing the line
        j = 0
        while j < len(line):
            # Ignore numbers or dashes at the beginning of list lines
            if is_list_item and not in_list:
                j = len(line) - len(line.lstrip())
                in_list = True
            elif not is_list_item:
                in_list = False
            
            # Simuler la frappe d'un caractère
            keyboard.press(line[j])
            keyboard.release(line[j])
            time.sleep(FAST_TYPING_DELAY)
            char_count += 1  # Incrémentez le compteur de caractères
            
            # Vérifiez si le nombre de caractères tapés atteint la limite
            if char_count >= CHARACTER_PAUSE_LIMIT:
                time.sleep(CHARACTER_PAUSE_DURATION)  # Pause
                char_count = 0  # Réinitialisez le compteur
            
            j += 1
        
        # Handle line breaks and formatting
        if i < len(lines) - 1:  # Check if there is a next line
            next_line = lines[i + 1]
            next_is_list_item = next_line.lstrip().startswith(('-', '*')) or (next_line.lstrip() and next_line.lstrip()[0].isdigit() and '.' in next_line.lstrip()[:3])
            
            if line.startswith("#"):
                # One line break after titles
                time.sleep(BEFORE_ENTER_DELAY)  # Délai avant d'appuyer sur entrée
                keyboard.press(Key.space)  # Appuyer sur espace
                keyboard.release(Key.space)
                time.sleep(FAST_TYPING_DELAY)  # Délai après espace
                keyboard.press(Key.backspace)  # Appuyer sur backspace
                keyboard.release(Key.backspace)
                time.sleep(FAST_TYPING_DELAY)  # Délai après backspace
                keyboard.press(Key.enter)  # Appuyer sur entrée
                keyboard.release(Key.enter)
                time.sleep(AFTER_ENTER_DELAY)
            
            elif is_list_item or is_task_item:
                # One line break after each list item
                time.sleep(BEFORE_ENTER_DELAY)  # Délai avant d'appuyer sur entrée
                keyboard.press(Key.space)  # Appuyer sur espace
                keyboard.release(Key.space)
                time.sleep(FAST_TYPING_DELAY)  # Délai après espace
                keyboard.press(Key.backspace)  # Appuyer sur backspace
                keyboard.release(Key.backspace)
                time.sleep(FAST_TYPING_DELAY)  # Délai après backspace
                keyboard.press(Key.enter)  # Appuyer sur entrée
                keyboard.release(Key.enter)
                time.sleep(AFTER_ENTER_DELAY)

                keyboard.press(Key.backspace)
                keyboard.release(Key.backspace)
                time.sleep(FAST_TYPING_DELAY)
            elif line.startswith(DIVIDER_STRING):  # Condition pour les diviseurs
                # Ne pas effacer le diviseur
                time.sleep(BEFORE_ENTER_DELAY)  # Délai avant d'appuyer sur entrée
                keyboard.press(Key.enter)  # Appuyer sur entrée
                keyboard.release(Key.enter)
                time.sleep(AFTER_ENTER_DELAY)
            elif line.startswith(">"):
                # No additional line break for quotes
                pass
            else:
                # One line break for other cases
                time.sleep(BEFORE_ENTER_DELAY)  # Délai avant d'appuyer sur entrée
                keyboard.press(Key.space)  # Appuyer sur espace
                keyboard.release(Key.space)
                time.sleep(FAST_TYPING_DELAY)  # Délai après espace
                keyboard.press(Key.backspace)  # Appuyer sur backspace
                keyboard.release(Key.backspace)
                time.sleep(FAST_TYPING_DELAY)  # Délai après backspace
                keyboard.press(Key.enter)  # Appuyer sur entrée
                keyboard.release(Key.enter)
                time.sleep(AFTER_ENTER_DELAY)
    
    simulating = False
    print("Simulation completed!")
    
    # Avant d'appuyer sur la touche entrée, ajoutez le délai
    time.sleep(BEFORE_ENTER_DELAY)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    time.sleep(FAST_TYPING_DELAY)  # Délai après espace 
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    
    
    
def on_press(key):
    global running, simulating
    if key == Key.f8:  # F8 to start the simulation
        if not simulating:
            simulating = True
            text = get_text()
            threading.Thread(target=simulate_typing, args=(text,)).start()
    elif key == Key.f9:  # F9 to stop the ongoing simulation
        simulating = False
        print("Stopping the ongoing simulation...")
    elif key == Key.f10:  # F10 to stop the program
        running = False
        print("Stopping the program...")
        return False  # Stop the listener

def main():
    global running
    print("Press F8 to simulate typing the text...")
    print("Press F9 to stop the ongoing simulation...")
    print("Press F10 to exit the program...")
    
    # Start the listener to listen for key presses
    with Listener(on_press=on_press) as listener:
        while running:
            time.sleep(0.1)
        listener.stop()
if __name__ == "__main__":
    main()