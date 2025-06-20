from tkinter import messagebox

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        messagebox.showwarning(title="Wystąpił błąd", message="Wiek nie jest liczbą")
        return False

def city_not_found_message():
    messagebox.showwarning(title="Wystąpił błąd", message="Nie znaleziono miasta")

def are_params_filled(*args):
    for arg in args:
        if arg is None or arg =='' or arg ==0:
            messagebox.showwarning(title="Wystąpił błąd", message="Nie podano wszystkich danych")
            return False
    return True