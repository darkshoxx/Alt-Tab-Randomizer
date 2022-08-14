from typing import List
import win32.win32gui as gui
import win32process as processes
import win32api as api
import win32con as con
import pywintypes

####################
# Global constants #
####################

# ScummVM handles that aren't the game.
LIST_OF_WRONG_WINDOWS = [
    "MSCTFIME UI",
    "Default IME",
    "ScummVM Status Window",
    "__wglDummyWindowFodder",
    "NVOGLDC invisible",
]
# required for usage of api.OpenProcess()
QUERY_INFO = con.PROCESS_QUERY_INFORMATION
VM_READ = con.PROCESS_VM_READ

def check_for_active_handles(handle_list:list[int])-> list:
    """Helper function to check whether all handles given are still alive
    Args:
        handle_list (list): list of handles to be checked.
    Returns:
        list of handles that have died (may be empty)"""
    dead_handles = []
    handles = get_all_handles()
    for check_handle in handle_list:
        if not(check_handle in handles):
            dead_handles.append(check_handle)
    return dead_handles


def write_to_file(string: str, filename: str) -> None:
    """Helper function to overwrite the text in a file that exists, or create
    said file with that content
    Args:
        string (str): text to be written to file.
        filename (str): string of path to file, or just filename.
    Returns:
        None"""
    with open(filename, mode="w") as file_object:
        file_object.write(string)


def get_all_handles() -> List:
    """Returns a list of all handles. Obtains curent foreground window and
    iterates through windows in front and behind."""
    current_handle = gui.GetForegroundWindow()
    list_of_handles = [current_handle]
    next_handles = get_half_handles(current_handle, "next")
    previous_handles = get_half_handles(current_handle, "previous")
    list_of_handles += next_handles
    list_of_handles += previous_handles
    return list_of_handles


def get_half_handles(current_handle: List[int], direction: str) -> List[int]:
    """Helper function to iterate over all handles in front/behind the active
    window handle.
    Args:
        current_handle (List[int]): singleton list containing active window
        direction (str): next/previous for search direciton.
    Returns:
        half_handles_list (List[int]): collected list of handles."""
    if direction == "next":
        direction_int = 3
    elif direction == "previous":
        direction_int = 2
    else:
        raise Exception("Invalid search direction")
    got_a_new_window = True
    half_handles_list = []
    # filling the list using gui.GetWindow, which uses direction_int to specify
    # next or previous window.
    while got_a_new_window:
        current_handle = gui.GetWindow(current_handle, direction_int)
        if (current_handle not in half_handles_list) and current_handle != 0:
            half_handles_list.append(current_handle)
        else:
            got_a_new_window = False
    return half_handles_list


def filter_handles_by_exe_name(list_of_handles):
    """Helper function to remove all handles that do not originate from ScummVM
    Args:
        list_of_handles (List[int]): List of all handles
    Returns:
        scummvm_handles (List[int]): List of handles belonging to ScummVM."""
    scummvm_handles = []
    for handle in list_of_handles:
        ident_b = get_process_id_from_handle(handle)
        # TODO: Replace Try/except with something that doesn't raise an error
        try:
            exe_name = get_exe_from_process_id(ident_b)
        except pywintypes.error:
            # print("an error has occured")
            continue
        if exe_name[-11:] == "scummvm.exe":
            # removes handles that are from ScummVM but known not to be
            # the actual game window
            if gui.GetWindowText(handle) not in LIST_OF_WRONG_WINDOWS:
                scummvm_handles.append(handle)
                print(gui.GetWindowText(handle))
    return scummvm_handles


def get_process_id_from_handle(handle: int):
    """Gets process id from the window handle. Required to find exe
    Args:
        handle (int): handle to obtain id from
    Returns:
        ident_b: PID for exe
    """
    _, ident_b = processes.GetWindowThreadProcessId(handle)
    return ident_b


def get_exe_from_process_id(ident_b) -> str:
    """Gets the process handle from the PID, returns string of exe"""
    process_handle_b = api.OpenProcess(QUERY_INFO | VM_READ, False, ident_b)
    exe_name = processes.GetModuleFileNameEx(process_handle_b, 0)
    return exe_name
