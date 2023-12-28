import pygame
import win32api
import win32con
import win32gui
# Code borrowed from: https://stackoverflow.com/questions/550001/fully-transparent-windows-in-pygame

TRANSPARENT = (55, 155, 255)  # Transparency color

def set_window_transparent():
    # create layered window
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    # set window transparency color
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*TRANSPARENT), 0, win32con.LWA_COLORKEY)
    
    # keep window on top
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)
    
def get_taskbar_height():

    monitor_info = win32api.GetMonitorInfo(win32api.MonitorFromPoint((0,0)))
    monitor_area = monitor_info.get("Monitor")
    work_area = monitor_info.get("Work")
    return monitor_area[3]-work_area[3]