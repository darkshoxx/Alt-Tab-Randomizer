import win32gui as w
import win32process as processes
import win32api as api
import win32con as con
import win32com.client as the_client
import pywintypes
import time
import random


current_handle = w.GetForegroundWindow()
list_of_handles = [current_handle]
got_a_new_window = True
while(got_a_new_window):
    #print(list_of_handles)
    current_handle = w.GetWindow(current_handle, 3)
    if (current_handle not in list_of_handles) and current_handle != 0:
        list_of_handles.append(current_handle)
    else:
        got_a_new_window = False
current_handle = w.GetWindow(w.GetForegroundWindow(),2)
got_a_new_window = True
while(got_a_new_window):
    #print(list_of_handles)
    current_handle = w.GetWindow(current_handle, 2)
    if (current_handle not in list_of_handles) and current_handle != 0:
        list_of_handles.append(current_handle)
    else:
        got_a_new_window = False

query_info = con.PROCESS_QUERY_INFORMATION
vm_read = con.PROCESS_VM_READ
scummvm_handles = []
known_wrong_window_names = [
    "MSCTFIME UI",
    "Default IME",
    "ScummVM Status Window",
    "__wglDummyWindowFodder",
    "NVOGLDC invisible"
    ]
for handle in list_of_handles:
    _, ident_b = processes.GetWindowThreadProcessId(handle)
    try:
        process_handle_b = api.OpenProcess(query_info | vm_read, False, ident_b)
        exe_name = processes.GetModuleFileNameEx(process_handle_b, 0)
    except pywintypes.error:
        #print("an error has occured")
        continue
    if exe_name[-11:] == "scummvm.exe":
        #print(w.GetWindowText(handle))
        if w.GetWindowText(handle) not in known_wrong_window_names:
            scummvm_handles.append(handle)
            #print(exe_name)
            print(w.GetWindowText(handle))
def choose_games_prompt():
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
            window_name = w.GetWindowText(item)
            window_selection_string += f"{i}) {window_name}\n"
        choice = input(window_selection_string)
        if choice == "0":
            return None
        int_choice = int(choice)
        if int_choice <= i:
            chosen_handles.append(scummvm_handles[int_choice - 1])
            print(f"you have chosen {w.GetWindowText(scummvm_handles[int_choice - 1])}")
            scummvm_handles.remove(scummvm_handles[int_choice - 1])
            choice = input("press enter to choose another game. type 'y' to end.")
            if i == 1 or choice == "y":
                return chosen_handles

def random_runner(chosen_list, min=None, max=None):
    if min is None:
        min = int(input("what is the minimum number of seconds on the same game?"))
    if max is None:
        max = int(input("what is the maximum number of seconds on the same game?"))
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
        w.SetForegroundWindow(next_game)



#w.SetForegroundWindow(177803456)
#[177803456, 1446768, 1577574]
#[177803456, 1577574]
chosen_list = choose_games_prompt()
if len(chosen_list)<2:
    raise Exception("need 2 games at least")
print(chosen_list)
random_runner(chosen_list)



