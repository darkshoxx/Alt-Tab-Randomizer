from logging import exception
from msilib.schema import Error
from typing import List
import click
import win32.win32gui as gui
import win32com.client as the_client
import pywintypes

import time
import random

from randomizer.utils import get_all_handles, filter_handles_by_exe_name


def choose_games_prompt(scummvm_handles: List) -> List:
    """Creates a list of all handles that belong to ScummVM games, and makes
    the user choose a sublist of at least two.
    Args:
        scummvm_handles (List): list of handles belonging to ScummVM
    Returns:
        chosen_handles (List): list of hadles of the chosen games."""
    chosen_handles = []
    choice = ""

    # Opening prompt with abort option
    while choice in ["", "n"]:
        choice = input("Dear user, would you like to select games? [y]/n\n")
        if choice == "":
            choice = "y"
        if choice == "":
            return None

    # Selection of games, with abort option
    choice = ""
    while choice in ["", "n", "0"]:

        window_selection_string = "Please select one of these windows"
        window_selection_string += " to add to the rando:\n"
        window_selection_string += "0) I have selected all the games\n"

        # Listing all game names that haven't been chosen yet
        for i, item in enumerate(scummvm_handles, start=1):
            window_name = gui.GetWindowText(item)
            window_selection_string += f"{i}) {window_name}\n"
        choice = input(window_selection_string)
        if choice == "0":
            return chosen_handles
        int_choice = int(choice)
        if int_choice <= i:
            # Adding to chosen handles
            chosen_handles.append(scummvm_handles[int_choice - 1])
            print(
                f"""you have chosen {
                    gui.GetWindowText(scummvm_handles[int_choice - 1])
                    }"""
            )
            # removing from list of options
            scummvm_handles.remove(scummvm_handles[int_choice - 1])
            choice = input("press enter to choose next game. type 'y' to end.")
            if i == 1 or choice == "y":
                return chosen_handles

        # Choice invalid
        print("Invalid choice, please try again\n")


def random_runner(
    chosen_list: List,
    min: int = None,
    max: int = None,
    remove_current_game: bool = None,
    mode: str = None,
):
    """Randomly resetting loop. Chooses random next game to display. Time until
    next reset is randomly chosen between min and max seconds.
    Args:
        chosen_list (List): list of handles belonging the chosen games.
        min (int): minimal number of seconds before window switch
        max (int): maximal number of seconds before window switch
        remove_current_game (bool): allowing to remain in the same game.
        mode (str): "seconds" or "clicks"
    """
    # Setting non-default values via prompts
    if min is None:
        min = int(input("minimum number of seconds on the same game?"))
    if max is None:
        max = int(input("maximum number of seconds on the same game?"))
    if remove_current_game is None:
        remove_current_game = not bool(
            input("Do you allow staying in the same game? (default = n)")
        )
    if mode is None:
        mode = (
            input("random time: [seconds]\n random clicks: clicks")
        )
        if mode != "clicks":
            mode = "seconds"
    shell = the_client.Dispatch("WScript.Shell")
    # Start with first entry on list
    current_handle = chosen_list[0]
    # TODO:check_window_validity(active_game_list)
    # closing windows removes them from chosen list.
    while len(chosen_list) > 1:
        if mode == "seconds":
            # get time for random sleeps.
            float_random = random.uniform(min, max)
            time.sleep(float_random)
        elif mode == "clicks":
            click_limit = random.choice(range(min, max))
            while click_limit > 0:
                wait_for_click()
                click_limit -= 1
        else:
            raise Exception("invalid mode")

        # using a sliced copy of all games to modify later.
        active_game_list = chosen_list[:]
        # Optionally removing current game.
        if remove_current_game and (current_handle in active_game_list):
            active_game_list.remove(current_handle)
        # TODO: check_window_validity(active_game_list)
        print(active_game_list)
        next_game = random.choice(active_game_list)
        print(next_game)
        # required to fix a bug with active windows.
        # Maybe better solutions exist.
        shell.SendKeys("%")
        current_handle = next_game
        # Choose next window, start over.
        try:
            gui.SetForegroundWindow(next_game)
        except pywintypes.error:
            chosen_list.remove(next_game)
            print(f"Warning, game {next_game} was closed.")
    while len(chosen_list) == 1:
        # very lazy way of checking that the window is still open
        print(f"Final Game {next_game} is still running.")
        time.sleep(5)
        try:
            gui.SetForegroundWindow(chosen_list[0])
        except pywintypes.error:
            chosen_list.remove(chosen_list[0])
            print(f"Final Game {next_game} was closed.")
    print("randomizer run ended successfully")

def wait_for_click():
    # TODO: wait for click function
    pass

def check_window_validity(active_game_list):
    pass


if __name__ == "__main__":
    """Acutal execution. Obtains all handles, filters to get the ones
    from ScummVM, prompts user to choose, starts random_runner."""
    list_of_all_handles = get_all_handles()
    scummvm_handles = filter_handles_by_exe_name(list_of_all_handles)
    chosen_list = choose_games_prompt(scummvm_handles)
    if len(chosen_list) < 2:
        raise Exception("need 2 games at least")
    print(chosen_list)
    random_runner(chosen_list)
