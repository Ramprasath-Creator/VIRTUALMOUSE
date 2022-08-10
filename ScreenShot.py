import pyautogui
from datetime import datetime
import numpy as np
import cv2
from win10toast import ToastNotifier
def takeScreenShot(fileLoc):
    toast = ToastNotifier()
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    now = datetime.now()
    current_time = now.strftime("%d_%m_%Y_%H_%M_%S")
    filename = fileLoc+'%s.png' % current_time

    if not cv2.imwrite(filename, image):
        raise Exception("Could not write image")
    else:
        toast.show_toast("ScreenShot","Saved successfully",duration=2, icon_path = "select.ico")