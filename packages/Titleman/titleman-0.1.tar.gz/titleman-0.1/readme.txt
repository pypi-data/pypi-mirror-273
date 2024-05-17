Titleman customizeds the titlebar of your app.
Code:
import Titleman as title
import tkinter as tk
from tkinter import ttk
root = tk.Tk()
clr = input("Enter color of titlebar ").lower()
root.geometry("200x200")
root.title("Titleman demo")
title.initCustom(root)
title.startTitlebar(root,clr)

root.mainloop()
------------------------------------------------------------------
Sorry this is a plain text file. I'm in a hurry.