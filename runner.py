
import win32.win32gui as gui
import win32com.client as the_client

import time
import random

from utils import get_all_handles, filter_handles_by_exe_name

LIST_OF_WRONG_WINDOWS = [
    "MSCTFIME UI",
    "Default IME",
    "ScummVM Status Window",
    "__wglDummyWindowFodder",
    "NVOGLDC invisible"
    ]

def choose_games_prompt(scummvm_handles):
    chosen_handles = []
    choice = ""
    while choice in ["", "n"]:
        choice = input("Dear user, would you like to select games? [y]/n\n")
        if choice == "":
            choice = "y"
        if choice == "":
            return None
    choice = ""
    while choice in ["", "n", "0"]:

        window_selection_string = "Please select one of these windows to add to the rando:\n"
        window_selection_string += "0) Abort\n"
        for i, item in enumerate(scummvm_handles, start=1):
            window_name = gui.GetWindowText(item)
            window_selection_string += f"{i}) {window_name}\n"
        choice = input(window_selection_string)
        if choice == "0":
            return chosen_handles
        int_choice = int(choice)
        if int_choice <= i:
            chosen_handles.append(scummvm_handles[int_choice - 1])
            print(f"you have chosen {gui.GetWindowText(scummvm_handles[int_choice - 1])}")
            scummvm_handles.remove(scummvm_handles[int_choice - 1])
            choice = input("press enter to choose another game. type 'y' to end.")
            if i == 1 or choice == "y":
                return chosen_handles

def random_runner(chosen_list, min=None, max=None, remove_current_game=None):
    if min is None:
        min = int(input("what is the minimum number of seconds on the same game?"))
    if max is None:
        max = int(input("what is the maximum number of seconds on the same game?"))
    if remove_current_game is None:
        remove_current_game = not bool(input("Do you allow staying in the same game? (default = n)"))

    shell = the_client.Dispatch("WScript.Shell")
    current_handle = chosen_list[0]
    while True:
        active_game_list = chosen_list[:]
        float_random = random.uniform(min, max)
        if remove_current_game and (current_handle in active_game_list):
            active_game_list.remove(current_handle)
        print(active_game_list)
        next_game = random.choice(active_game_list)
        print(next_game)
        time.sleep(float_random)
        shell.SendKeys('%')
        current_handle = next_game
        gui.SetForegroundWindow(next_game)

if __name__ == "__main__":

    list_of_all_handles = get_all_handles()
    scummvm_handles = filter_handles_by_exe_name(list_of_all_handles)
    chosen_list = choose_games_prompt(scummvm_handles)
    if len(chosen_list)<2:
        raise Exception("need 2 games at least")
    print(chosen_list)
    random_runner(chosen_list)



