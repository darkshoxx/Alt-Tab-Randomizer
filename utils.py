from typing import List
import win32.win32gui as gui
import win32process as processes
import win32api as api
import win32con as con
import pywintypes

### Global constants

QUERY_INFO = con.PROCESS_QUERY_INFORMATION
VM_READ = con.PROCESS_VM_READ

def get_all_handles() -> List:
    """Returns a list of all handles"""
    current_handle = gui.GetForegroundWindow()
    list_of_handles = [current_handle]
    next_handles = get_half_handles(current_handle, "next")
    previous_handles = get_half_handles(current_handle, "previous")
    list_of_handles += next_handles
    list_of_handles += previous_handles
    return list_of_handles

def get_half_handles(current_handle, direction):
    if direction == "next":
        direction_int = 3
    elif direction == "previous":
        direction_int = 2
    else:
        raise Exception("Invalid search direction")
    got_a_new_window = True
    half_handles_list = []
    while(got_a_new_window):
        current_handle = gui.GetWindow(current_handle, direction_int)
        if (current_handle not in half_handles_list) and current_handle != 0:
            half_handles_list.append(current_handle)
        else:
            got_a_new_window = False
    return half_handles_list

def filter_handles_by_exe_name(list_of_handles):
    scummvm_handles = []
    for handle in list_of_handles:
        _, ident_b = processes.GetWindowThreadProcessId(handle)
        # TODO: Replace Try/except with something that doesn't raise an error
        try:
            process_handle_b = api.OpenProcess(QUERY_INFO | VM_READ, False, ident_b)
            exe_name = processes.GetModuleFileNameEx(process_handle_b, 0)
        except pywintypes.error:
            #print("an error has occured")
            continue
        if exe_name[-11:] == "scummvm.exe":
            if gui.GetWindowText(handle) not in LIST_OF_WRONG_WINDOWS:
                scummvm_handles.append(handle)
                print(gui.GetWindowText(handle))
    return scummvm_handles