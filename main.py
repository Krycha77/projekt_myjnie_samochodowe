from tkinter import *
import tkintermapview
from tkinter import ttk
from carwash import *
from employee import *

root = Tk()
root.geometry("1400x800")
root.title('CarWash Manager')

tabControl = ttk.Notebook(root)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)

configure_carwash_gui(tab1)
configure_employee_gui(tab2)

tabControl.add(tab1, text ='Myjnie')
tabControl.add(tab2, text ='Pracownicy')
tabControl.pack(expand = 1, fill ="both")

root.mainloop()