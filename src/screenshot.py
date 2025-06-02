import platform
import numpy as np

if platform.system() == "Windows":
    import mss
elif platform.system() == "Linux":
    import mss
else:
    import mss

def capture_screenshot(window_handle=None, region=None):
    """
    Capture a screenshot of the specified region.
    If region is None, capture the entire screen.
    region: dict with keys 'x', 'y', 'w', 'h'
    """
    with mss.mss() as sct:
        if region:
            monitor = {
                "left": region["x"],
                "top": region["y"],
                "width": region["w"],
                "height": region["h"]
            }
        else:
            monitor = sct.monitors[1]  # Primary monitor

        sct_img = sct.grab(monitor)
        img = np.array(sct_img)
        # mss returns BGRA, convert to BGR
        img = img[:, :, :3]
        return img