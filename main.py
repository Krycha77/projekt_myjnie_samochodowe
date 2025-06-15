from tkinter import *
import tkintermapview
from tkinter import ttk
from carwash import *

root = Tk()
root.geometry("1400x800")
root.title('CarWash Manager')

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)

configure_gui(tab1)


tabControl.add(tab1, text ='Myjnie')
tabControl.pack(expand = 1, fill ="both")

root.mainloop()