from ctypes import *
import thread
import time

###############################################################################
###############################################################################

MOUSEEVENTF_LEFTDOWN = 2
MOUSEEVENTF_LEFTUP   = 4

KEYCODE_LBUTTON = 0x01
KEYCODE_RBUTTON = 0x02
KEYCODE_MBUTTON = 0x04
KEYCODE_ALT = 0xA4
KEYCODE_F1 = 0x70

###############################################################################
###############################################################################

class POINT(Structure):
    _fields_ = [("x", c_ulong),
                ("y", c_ulong)]

###############################################################################
###############################################################################

g_clicksPerSec = 20.0
g_clickFreq = 1.0 / g_clicksPerSec 
g_keyPressed = False
g_clickPos = POINT()

###############################################################################
###############################################################################

# see http://msdn.microsoft.com/en-us/library/ms646260(VS.85).aspx for details
def click(x, y):
    windll.user32.SetCursorPos(x, y)
    windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0,0) # left down
    windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0,0) # left up

def updateKeypress():
    global g_keyPressed

    while True:
        shortRes = windll.user32.GetAsyncKeyState(KEYCODE_F1) & windll.user32.GetAsyncKeyState(KEYCODE_ALT)
        g_keyPressed = True if ( shortRes & 0x8000 ) else False
        time.sleep(0.05)

def mouseDown():
    shortRes = windll.user32.GetAsyncKeyState(KEYCODE_LBUTTON) | windll.user32.GetAsyncKeyState(KEYCODE_RBUTTON) | windll.user32.GetAsyncKeyState(KEYCODE_MBUTTON)
    return True if ( shortRes & 0x8000 ) else False

def startAutoClicker():
    global g_clickPos
    global g_keyPressed 

    print "AutoClicker Start"
    g_keyPressed = False;
    windll.user32.GetCursorPos(byref(g_clickPos))
    time.sleep(0.5) # Avoid to stop directly

    while True:
        if g_keyPressed:
            print "AutoClicker Stop"
            return
        prevPos = POINT()

        if mouseDown():
            continue

        activeWindow = windll.user32.GetForegroundWindow ()
        windll.user32.GetCursorPos(byref(prevPos))

        click(g_clickPos.x, g_clickPos.y)

        windll.user32.SetForegroundWindow(activeWindow)
        windll.user32.SetCursorPos(prevPos.x, prevPos.y)
        time.sleep(g_clickFreq)


thread.start_new_thread(updateKeypress, ())

while True:
    if g_keyPressed:
        startAutoClicker()
        time.sleep(0.5) # Avoid to restart directly
    time.sleep(0.05)

