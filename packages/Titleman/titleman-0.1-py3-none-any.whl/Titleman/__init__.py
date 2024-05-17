
import tkinter as tk
from ctypes import windll
"""
Titleman--
This project is designed to customize the titlebar of a tkinter window.
"""
#Declare varibles
window_minimized = False
window_maxamized = False

def maxamize(root):
    global window_maxamized
    if window_maxamized == False:
         root.state("zoomed")
         window_maxamized = True
    else:
        root.state("normal")
        window_maxamized = False
#I found this on a StackOverflow thread:https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter... Added the root finding myself
def move_window(event):
    root = event.widget.winfo_toplevel()
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))
#RELLY GREAT GITHUB REPO WITH THIS CODE!
def set_appwindow(mainWindow:tk.Tk): # to display the window icon on the taskbar, 
                               # even when using root.overrideredirect(True
    # Some WindowsOS styles, required for task bar integration
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
   
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())    
def set_appwindow(mainWindow): # to display the window icon on the taskbar, 
                               # even when using root.overrideredirect(True)
    # Some WindowsOS styles, required for task bar integration
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    # Magic
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
   
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())
# To minimize the window
def minimize(root): #https://github.com/Terranova-Python/Tkinter-Menu-Bar/blob/main/main.py
    global window_minimized
    if window_minimized == False:
        root.attributes("-alpha",0)
        window_minimized = True
    else:
        root.focus()
        root.attributes("-alpha",1)
        window_minimized = False
def initCustom(root:tk.Tk):#Create function to remove titlebar, set titleman icon, and show the icon
        root.overrideredirect(True)
        root.iconbitmap("icon.ico")
        set_appwindow(root)
def startTitlebar(root:tk.Tk,color:str):#Function to start titlebar
    #NOTE: Once run, you cannot use grid or place as geometry managers.
    #TODO: Figure out how to use multiple geometry managers in one window
    # Get title text
    titleText = root.title()
    # Get icon color
    iconColor = None
    if color == "white":
        iconColor = "black"
    else:
        iconColor = "white"
    # Create icons and frame
    titlebar = tk.Frame(root,bg=color)
    titlebar.pack(side=tk.TOP,fill=tk.X)
    btnFrame = tk.Frame(titlebar)
    close = tk.Button(btnFrame,fg="white",bg="red" ,text="X",command=lambda:root.quit())
    maxamize_btn = tk.Button(btnFrame,fg=iconColor,bg=color ,text="𑨠",command=lambda:maxamize(root)) #I added the _btn part because of an error: "Button object is not callable":) FOR DEVS: ICON APPEARS INVISIBLE TO VISUAL STUDIO!
    minamize_btn = tk.Button(btnFrame,fg=iconColor,bg=color ,text="-",command=lambda:minimize(root))
    minamize_btn.pack(side=tk.RIGHT)
    btnFrame.pack(side=tk.RIGHT,fill=tk.Y)
    close.pack(side=tk.LEFT)
    maxamize_btn.pack()
    root.bind("<B1-Motion>",move_window)
    title = tk.Label(titlebar,text=titleText,fg=iconColor,bg=color)
    title.pack(side=tk.LEFT)
    
     
