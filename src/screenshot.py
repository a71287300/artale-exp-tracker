import win32gui
import win32ui
import win32con
import numpy as np
from ctypes import windll

def capture_screenshot(window_handle):
    """Capture a screenshot of the specified window."""
    try:
        # Get window dimensions
        left, top, right, bottom = win32gui.GetWindowRect(window_handle)
        width = right - left
        height = bottom - top

        # Create device context and bitmap
        hwnd_dc = win32gui.GetWindowDC(window_handle)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        
        # Create bitmap object
        save_bitmap = win32ui.CreateBitmap()
        save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(save_bitmap)

        # Copy screen into bitmap
        result = windll.user32.PrintWindow(window_handle, save_dc.GetSafeHdc(), 2)
        
        if result != 1:
            raise Exception(f"PrintWindow failed with result {result}")

        # Convert bitmap to numpy array
        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmpstr, dtype='uint8')
        img = img.reshape((height, width, 4))

        # Cleanup
        win32gui.DeleteObject(save_bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(window_handle, hwnd_dc)

        # Convert from BGRA to BGR
        return img[:, :, :3]

    except Exception as e:
        print(f"Screenshot error: {e}")
        return None