import win32gui
import win32con
import win32api  # Add this import
from typing import Optional, Tuple

def get_window(window_name: str) -> Optional[int]:
    """Find window by name and return its handle."""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if window_name.lower() in window_text.lower():
                windows.append(hwnd)
        return True

    windows = []
    win32gui.EnumWindows(callback, windows)
    return windows[0] if windows else None

def get_active_windows():
    """Get a list of all active window titles."""
    window_titles = []
    def enum_window_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                window_titles.append(title)
    win32gui.EnumWindows(enum_window_callback, None)
    return sorted(window_titles)

def get_experience_region(window_handle: int) -> Tuple[int, int, int, int]:
    """Get the region of the window where experience is displayed."""
    if not window_handle:
        return (0, 0, 0, 0)
    
    # Get window dimensions
    left, top, right, bottom = win32gui.GetWindowRect(window_handle)
    width = right - left
    height = bottom - top
    
    # Assuming experience is typically shown in the top-right corner
    # Adjust these values based on the specific game
    exp_width = width // 4
    exp_height = height // 6
    return (right - exp_width, top, right, top + exp_height)

def bring_window_to_front(window_handle: int) -> None:
    """Bring the window to the foreground."""
    if window_handle:
        try:
            # Get the window's current state
            window_placement = win32gui.GetWindowPlacement(window_handle)
            
            # Check if window is minimized
            if window_placement[1] == win32con.SW_SHOWMINIMIZED:
                win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
            
            # Try to force the window to foreground
            foreground_window = win32gui.GetForegroundWindow()
            if foreground_window != window_handle:
                # Simulate Alt key press to allow window switching
                win32api.keybd_event(0x12, 0, 0, 0)  # Alt key down
                win32gui.SetForegroundWindow(window_handle)
                win32api.keybd_event(0x12, 0, 0x0002, 0)  # Alt key up
                
            # Additional attempt to activate the window
            win32gui.BringWindowToTop(window_handle)
            win32gui.SetActiveWindow(window_handle)
            
        except Exception as e:
            print(f"Error bringing window to front: {e}")