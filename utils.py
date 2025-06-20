from tkinter import messagebox

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        messagebox.showwarning(title="Wystąpił błąd", message="wiek nie jest liczbą")
        return False

def city_not_found_message():
    messagebox.showwarning(title="Wystąpił błąd", message="nie znaleziono miasta")