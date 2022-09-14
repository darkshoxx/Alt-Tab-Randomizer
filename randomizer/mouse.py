from randomizer.utils import filter_handles_by_exe_name, get_all_handles
import win32ui
import win32con
import win32api

list_of_all_handles = get_all_handles()
scummvm_handles, handles_dict = filter_handles_by_exe_name(list_of_all_handles)
print(handles_dict)
# for today:
# Myst 7472942
# Riven 197586
win = win32ui.CreateWindowFromHandle(7472942)
win.SendMessage(7472942, win32con.WM_MOUSEMOVE, win32api.MAKELONG(50,50))