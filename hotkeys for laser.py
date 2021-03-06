'''

HOTKEYS FOR LASER

Programmed by Brock Brown for Signet Jewelers
Github repository is located at https://github.com/brockbrownwork/hotkeys_for_laser

For information, support, or feature requests contact Brock at brockbrownwork@gmail.com

'''


# this is a wrapper for pyautogui, simplifies some of the function calls
from bot import search_and_click, found, find, click_if_exists, hover_over, center_mouse
# this is for detecting keystrokes
import keyboard
# for waiting and measuring how long hotkey functions take
from time import sleep, time
# for copy/paste functionality
from pyperclip import copy, paste
# for clickbotting and emulating keystrokes
import pyautogui
# for listing the files in a directory, used in the search function
from os import listdir
# this is to make sure that there's only one instance of the program running at a time
from tendo import singleton
# this is for the search functionality to figure out how similar one string is to another
from difflib import SequenceMatcher
# ooh boy threading
from threading import Thread
# alright let's try queueing again
from global_hotkeys import register_hotkeys, start_checking_hotkeys
from queue import Queue

try:
    # Singleton makes sure that there's only one instance of this program
    # running at a time so that they don't step on each other's toes
    me = singleton.SingleInstance()
except:
    # Warns the user that there's another instance running and aborts the program
    pyautogui.alert(title = "hey dummy",
                    text = "There's already one running :)")
    quit()

# for input validation
def is_type(value, type_name):
    try:
        type_name(value)
        return True
    except ValueError as e:
        return False

# Load up the hotkeys defined in "settings.txt", these are ctrl + 1, ...
settings = {}
with open("settings.txt") as f:
    text = f.read().split("\n")
    for line in text:
        key, file_name = line.split(":")
        settings[key] = file_name

def similar_function_generator(query):
    # lambda function generator for the similar function
    # this is used to allow the "sorted" function to be able to sort by similarity
    return lambda x: similar(query, x)
def similar(a, b):
    # this function figures approximates how similar one string is to another
    # 0 = no similarity, 1 = exact copy
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def solve_rotational_shenanigans():
    '''
    This (hopefully) solves the issues with rotating the ring then suddenly
    stamping after the job. >.>
    '''
    if not found("images\\selected_execute.png"):
        search_and_click("images\\execute.png")
    sleep(0.2)
    search_and_click("images\\show_position_start.png")
    hover_over("images\\right_arrow.png")

def change_text():
    '''
    Changes the text of the first object in the layout.
    '''
    click_if_exists("images\\layout.png")
    click_if_exists("images\\text_field.png")
    pyautogui.hotkey("ctrl", "a")

def search():
    '''
    Search for a template. Simply type in part of the name of
    the template you're trying to pull up. Example: 'lov' will pull up the
    Vera Wang Love stamp.
    '''
    files = listdir("C:\\Users\\ghopper\\Desktop\\stamps\\new computer")
    # ask for the name of the template
    query = pyautogui.prompt(text = "What template do you need?")
    found_files = []
    exact_file = None
    found_file = None
    # if the user doesn't say anything, return nothing
    if not query:
        return None
    # for each of the files in the folder, see if part of the query
    # is in the file name, then put it in a list
    for file in files:
        if query.lower() in file.lower():
            found_files.append(file)
    if query.lower() in [i.split('.')[0].lower() for i in files]:
        exact_file = query
    # if there's no possible candidates, give the user a list of the top 10 most similar files
    if len(found_files) == 0:
        most_similar_files = sorted(files, key = similar_function_generator(query))[::-1]
        prompt = f"Couldn't find {query}, here are the ten most similar names:\n"
        for i, file in enumerate(most_similar_files[:10]):
            prompt += f'{i + 1}: {file}\n'
        choice = pyautogui.prompt(text = prompt)
        if choice == "":
            choice = 1
        elif not is_type(choice, int):
            return None
        choice = int(choice)
        found_file = most_similar_files[choice - 1]
    # if there's a template by the exact name the user typed, give it to em
    if exact_file:
        found_file = exact_file
    # if there's only one possible candidate, give them that template
    elif len(found_files) == 1:
        found_file = found_files[0]
    # if there's more than one possibility, give the user a choice
    elif len(found_files) > 1:
        prompt = 'Which one you want?\n'
        for i, file in enumerate(found_files):
            prompt += f'{i + 1}: {file}\n'
        choice = pyautogui.prompt(text = prompt)
        if choice == "":
            choice = 1
        choice = int(choice)
        found_file = found_files[choice - 1]
    # if the template is found, go open the template
    if found_file:
        while True:
            if click_if_exists("images\\file.png", go_back = False):
                break
            if click_if_exists("images\\underlined_file.png", go_back = False):
                break
        while not found("images\\open.png"):
            pyautogui.click() # TODO: fix this truly horrendous code (YUCK!)
        sleep(0.1)
        pyautogui.hotkey("o")
        copy(f"C:\\Users\\ghopper\\Desktop\\stamps\\new computer\\{found_file}")
        pyautogui.hotkey("ctrl", "v")
        pyautogui.hotkey("enter")
        # select the inside diameter so the user can change it if they want
        change_inside_diameter()
    print("")

def change_alpha():
    '''
    Rotates the stamp (not the ring).
    '''
    # if the layout isn't already selected, click it
    if not found("images\\selected_layout.png"):
        search_and_click("images\\layout.png")
    # click into the alpha parameter, then copy it
    search_and_click("images\\alpha.png", below = 20, double = True)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    # ask the user how much they'd like to turn, then add that to
    # the previous alpha value
    prompt = "How many degrees counterclockwise do you want to turn?"
    command = pyautogui.prompt(text = prompt, title = "LZR Hotkeys")
    if not is_type(command, float):
        return None
    copy(int(command) + int(paste()))
    pyautogui.hotkey("ctrl", "v")
    solve_rotational_shenanigans()

def flip_stamp():
    '''
    Rotates the first object in the layout 180 degrees.
    '''
    # if layout isn't already selected, click it
    if not found("images\\selected_layout.png"):
        search_and_click("images\\layout.png")
    # add 180 degrees to the alpha parameter
    search_and_click("images\\alpha.png", below = 20, double = True)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.hotkey("ctrl", "c")
    copy(str(int(paste()) + 180))
    sleep(0.1)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("enter")
    solve_rotational_shenanigans()

def close_door():
    '''
    Makes sure that the door is shut. This is a helper function for send_job.
    '''
    timeout = 15
    start = time()
    # while the door isn't closed, click the door button
    while not found("images\\closed.png"):
        if time() - start > timeout:
            raise Exception("Timed out, spent too much time looking for closed.png")
        if found("images\\could_not_be_closed.PNG"):
            break
        if found("images\\question_door.png"):
            if found("images\\could_not_be_closed.png"):
                break
            click_if_exists("images\\question_door.png", double = True)
        click_if_exists("images\\door.png", double = True)
    sleep(0.5)
    click_if_exists("images\\ok.png")
    solve_rotational_shenanigans()

def toggle_door():
    '''
    Opens the door if it's shut, closes the door if it's open.
    '''
    if click_if_exists("images\\question_door.png", double = True)\
       or click_if_exists("images\\door.png", double = True):
        print("found question door")
        close_door()
    elif click_if_exists("images\\closed.png", double = True):
        print("found closed!")
        click_if_exists("images\\closed.png", double = True)
        hover_over("images\\right_arrow.PNG")

last_measurement = 16

def change_inside_diameter():
    '''
    Goes to the layout, then clicks the inside diameter parameter so that it's
    ready to change.
    '''
    global last_measurement
    original_offset = -0.5
    offset = original_offset
    search_and_click("images\\surface.png")
    sleep(0.3)
    valid_input = False
    while not valid_input:
        try:
            dialogue = "Enter measurement (press enter to use last measurment, enter 'f' for flat engraving, 'e' for an enhancer) > "
            diameter = pyautogui.prompt(text = dialogue)
            diameter = diameter.lower()
            if diameter == None:
                return None
            # format the user's input so that...
            # - it adds a decimal point where there's one needed
            # - strips non numerical and non decimal point numbers
            # - gets rid of double instances of decimal points (common mistake)
            if diameter not in 'fe':
                diameter = ''.join([i for i in diameter if i.isdigit() or i == '.'])
            elif diameter == "f":
                offset = original_offset * -1
                continue
            elif diameter == "e":
                offset = original_offset - 1
                continue
            while '..' in diameter:
                diameter = diameter.replace('..', '.')
            if '.' not in diameter and len(diameter) >= 3:
                diameter = diameter[0:2] + '.' + diameter[2:]
            elif diameter == "":
                copy(str(last_measurement))
                break
            elif not is_type(diameter, float):
                print("Not a valid input, try again.")
                continue
            diameter = float(diameter)
            valid_input = True
            measurement = str(round(diameter + offset, 3))
            copy(measurement)
            last_measurement = measurement
        except ValueError as e:
            print("Not a valid float, please try again.")
    search_and_click("images\\inside_diameter.png")
    pyautogui.hotkey("ctrl", "v")

def open_template(key):
    '''
    Opens the respective template defined by settings.txt, i.e.: ctrl + 1 => 10k template
    '''
    print("hotkey pressed: ctrl + ", key)
    print("opening {0}...".format(settings[key]))
    start = time()
    search_and_click("images\\file.png", go_back = False)
    while not found("images\\open.png"):
        pyautogui.click() # TODO: fix this truly horrendous code
    sleep(0.1)
    pyautogui.hotkey('o')
    # search_and_click("images\\open.png", go_back = False)
    copy("C:\\Users\\ghopper\\Desktop\\stamps\\new computer\\{0}".format(settings[key]))
    pyautogui.hotkey("ctrl", "v")
    pyautogui.hotkey("enter")
    change_inside_diameter()
    execution_time = round(time() - start, 2)
    print(f"Done opening {settings[key]}, took {execution_time} seconds\n")

def send_job():
    '''
    Closes the door, fixes rotational shenanigans, then
    asks the user if they're ready to stamp.
    '''
    close_door()
    ready = pyautogui.confirm(text = "Send the job?", buttons = ["yes", "no"])
    if ready == "yes":
        click_if_exists("images\\execute.png")
        click_if_exists("images\\start.png", double = True)
        click_if_exists("images\\ok.PNG")

hotkey_to_function = {
        "ctrl + d" : toggle_door,
        "ctrl + shift + f" : flip_stamp,
        "ctrl + enter" : send_job,
        "ctrl + r" : change_alpha,
        "f2" : search,
        "ctrl + shift + t" : change_text,
        "ctrl + i" : change_inside_diameter
    }


bindings = []
for hotkey in hotkey_to_function:
    combo = [thing.strip() for thing in hotkey.split("+")]
    for index, thing in enumerate(combo):
        if thing == 'ctrl':
            combo[index] = 'control'
    print('combo: ', combo)
    bindings.append([combo, None, lambda: add_to_queue(hotkey_to_function[hotkey])])
register_hotkeys(bindings)
# start_checking_hotkeys() TODO


def caffiene():
    while True:
        sleep(60 * 5)
        pyautogui.hotkey("F15")
        print("Pressed F15 to stay awake!")
morning_coffee = Thread(target = caffiene)
morning_coffee.start()

hotkey_queue = Queue(maxsize = 3)
def add_to_queue(thing):
    if not hotkey_queue.full():
        hotkey_queue.put(thing)
def hotkey_handler():
    while True:
        print(hotkey_queue.get())

def main():
    '''
    This boots up the hotkey listener, ready to groove.
    '''
    start = time()
    while True:
        # wait 1/20th of a second to start again as not to gobble cpu
        sleep(0.05)
        for hotkey in hotkey_to_function:
            if keyboard.is_pressed(hotkey):
                start_of_function = time()
                center_mouse()
                function = hotkey_to_function[hotkey]
                print(f"{hotkey} pressed!: {function.__name__}")
                function()
                execution_time = round(time() - start_of_function, 2)
                print(f"Done with {function.__name__}, took {execution_time} seconds\n")
        # open respective template if ctrl + [custom character] is pressed
        for key in settings.keys():
            if keyboard.is_pressed('ctrl + {0}'.format(key)):
                center_mouse()
                open_template(key)

if __name__ == "__main__":
    justification = 30 # this is how far the columns get pushed apart.
    print("Hotkeys for LZR\n\n" + "Function".ljust(justification) + "Hotkey\n" + "=" * (justification + 10))
    for hotkey in sorted(hotkey_to_function):
        function = hotkey_to_function[hotkey]
        print((function.__name__ + ' ').ljust(justification - 1, '-') + ' ' + hotkey)
        if function.__doc__:
            print(function.__doc__[1:-1])

    print("ctrl + [a number] to open a template (see label below keyboard)")
    # Catch any error, state it, then ~ gracefully ~ restart the program
    while True:
        try:
            main()
        except Exception as e:
            print("Oh, boy: {0}\n".format(e))
            print("Restarted gracefully!")
