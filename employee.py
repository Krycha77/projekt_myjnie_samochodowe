from tkinter import *
from utils import is_integer, city_not_found_message

import tkintermapview

from tkinter import ttk

employees: list = []


class Employee:
    def __init__(self, first_name, last_name, age, carwash_name, city, widget):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.carwash_name = carwash_name
        self.city = city
        self.coordinates = self.get_coordinates()
        self.marker = widget.set_marker(self.coordinates[0], self.coordinates[1],
                                            text=f'{self.first_name} {self.last_name}, {self.age}, {self.carwash_name}, {self.city}')

    # FUNKCJA WEWNĄTRZ KLASY TO METODA
    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        adres_url: str = f'https://pl.wikipedia.org/wiki/{self.city}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')

        if len(response_html.select('.latitude'))<2:
            city_not_found_message()
            return

        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.')),
        ]



def configure_employee_gui(tab2: ttk.Frame) -> None:
    def add_employee() -> None:
        first_name = entry_pracownika_imie.get()
        last_name = entry_pracownika_nazwisko.get()
        age = entry_pracownika_wiek.get()
        employee_name = entry_pracownika_nazwa_myjni.get()
        city = entry_pracownika_miasto.get()

        if not is_integer(age):
            return

        employee = Employee(first_name=first_name, last_name=last_name, age=age, carwash_name=employee_name, city=city, widget=map_widget_pracownika)
        employees.append(employee)

       

        entry_pracownika_imie.delete(0, END)
        entry_pracownika_nazwisko.delete(0, END)
        entry_pracownika_wiek.delete(0, END)
        entry_pracownika_nazwa_myjni.delete(0, END)
        entry_pracownika_miasto.delete(0, END)

        entry_pracownika_imie.focus()
        show_employees()

    def show_employees():
        listbox_lista_pracownikow.delete(0, END)
        for idx, employee in enumerate(employees):
            listbox_lista_pracownikow.insert(idx, f'{idx + 1}. {employee.first_name} {employee.last_name} {employee.age} {employee.carwash_name} {employee.city}')

    def remove_employee():
        i = listbox_lista_pracownikow.index(ACTIVE)
        print(i)
        employees[i].marker.delete()
        employees.pop(i)
        show_employees()

    def edit_employee():
        i = listbox_lista_pracownikow.index(ACTIVE)
        first_name = employees[i].first_name
        last_name = employees[i].last_name
        age = employees[i].age
        carwash_name = employees[i].carwash_name
        city = employees[i].city

        entry_pracownika_imie.insert(0, first_name)
        entry_pracownika_nazwisko.insert(0, last_name)
        entry_pracownika_wiek.insert(0, age)
        entry_pracownika_nazwa_myjni.insert(0, carwash_name)
        entry_pracownika_miasto.insert(0, city)

        button_dodaj_pracownika.config(text='Zapisz', command=lambda: update_employee(i))

    def update_employee(i):
        first_name = entry_pracownika_imie.get()
        last_name = entry_pracownika_nazwisko.get()
        age = entry_pracownika_wiek.get()
        carwash_name = entry_pracownika_nazwa_myjni.get()
        city = entry_pracownika_miasto.get()

        if not is_integer(age):
            return

        employees[i].first_name = first_name
        employees[i].last_name = last_name
        employees[i].age = age
        employees[i].carwash_name = carwash_name
        employees[i].city = city


        employees[i].coordinates = employees[i].get_coordinates()
        employees[i].marker.delete()
        employees[i].marker = map_widget_pracownika.set_marker(employees[i].coordinates[0], employees[i].coordinates[1],
                                                           text=f'{employees[i].first_name} {employees[i].last_name} {employees[i].age} {employees[i].carwash_name} {employees[i].city}')

        show_employees()
        button_dodaj_pracownika.config(text='Dodaj', command=add_employee)

        entry_pracownika_imie.delete(0, END)
        entry_pracownika_nazwisko.delete(0, END)
        entry_pracownika_wiek.delete(0, END)
        entry_pracownika_nazwa_myjni.delete(0, END)
        entry_pracownika_miasto.delete(0, END)

        entry_pracownika_imie.focus()

    def show_employee_details():
        i = listbox_lista_pracownikow.index(ACTIVE)
        label_szczegoly_pracownika_imie_wartosc.config(text=employees[i].first_name)
        label_szczegoly_pracownika_nazwisko_wartosc.config(text=employees[i].last_name)
        label_szczegoly_pracownika_wiek_wartosc.config(text=employees[i].age)
        label_szczegoly_pracownika_nazwa_myjni_wartosc.config(text=employees[i].carwash_name)
        label_szczegoly_pracownika_miasto_wartosc.config(text=employees[i].city)


        map_widget_pracownika.set_zoom(15)
        map_widget_pracownika.set_position(employees[i].coordinates[0], employees[i].coordinates[1])



    ramka_lista_pracownikow = Frame(tab2)
    ramka_formularz_pracownikow = Frame(tab2)
    ramka_szczegoly_pracownika = Frame(tab2)
    ramka_mapa_pracownicy= Frame(tab2)

    ramka_lista_pracownikow.grid(row=0, column=0)
    ramka_formularz_pracownikow.grid(row=0, column=1)
    ramka_szczegoly_pracownika.grid(row=2, column=0, columnspan=2)
    ramka_mapa_pracownicy.grid(row=3, column=0, columnspan=2)

    button_dodaj_pracownika= Button(ramka_formularz_pracownikow, text='Dodaj', command=add_employee)
    button_dodaj_pracownika.grid(row=6, column=0, columnspan=2)


    label_lista_pracownika = Label(ramka_lista_pracownikow, text='Lista pracowników:')
    label_lista_pracownika.grid(row=0, column=0)

    listbox_lista_pracownikow = Listbox(ramka_lista_pracownikow, width=50, height=10)
    listbox_lista_pracownikow.grid(row=1, column=0, columnspan=3)

    button_pokaz_pracownika = Button(ramka_lista_pracownikow, text='Pokaż szczegóły', command=show_employee_details)
    button_pokaz_pracownika.grid(row=2, column=0)
    button_usun_pracownika = Button(ramka_lista_pracownikow, text='Usuń', command=remove_employee)
    button_usun_pracownika.grid(row=2, column=1)
    button_edytuj_pracownika = Button(ramka_lista_pracownikow, text='Edytuj', command=edit_employee)
    button_edytuj_pracownika.grid(row=2, column=2)

    label_formularz_pracownik = Label(ramka_formularz_pracownikow, text='Formularz:')
    label_formularz_pracownik.grid(row=0, column=0)

    label_szczegoly_pracownika_imie = Label(ramka_formularz_pracownikow, text='Imię:')
    label_szczegoly_pracownika_imie.grid(row=1, column=0, sticky=W)

    label_szczegoly_pracownika_nazwisko = Label(ramka_formularz_pracownikow, text='Nazwisko:')
    label_szczegoly_pracownika_nazwisko.grid(row=2, column=0, sticky=W)
    
    label_szczegoly_pracownika_wiek = Label(ramka_formularz_pracownikow, text='Wiek:')
    label_szczegoly_pracownika_wiek.grid(row=3, column=0, sticky=W)
    
    label_szczegoly_pracownika_miasto = Label(ramka_formularz_pracownikow, text='Miasto:')
    label_szczegoly_pracownika_miasto.grid(row=4, column=0, sticky=W)
    
    label_szczegoly_pracownika_myjnia = Label(ramka_formularz_pracownikow, text='Nazwa myjni:')
    label_szczegoly_pracownika_myjnia.grid(row=5, column=0, sticky=W)


    # Ramka_szczegoly_pracownika
    label_pokaz_szczegoly_pracownika = Label(ramka_szczegoly_pracownika, text='Szczegóły pracownika:')
    label_pokaz_szczegoly_pracownika.grid(row=0, column=0)

    label_szczegoly_pracownika_imie = Label(ramka_szczegoly_pracownika, text='Imię: ')
    label_szczegoly_pracownika_imie.grid(row=1, column=0, sticky=E)

    label_szczegoly_pracownika_imie_wartosc = Label(ramka_szczegoly_pracownika, text='....')
    label_szczegoly_pracownika_imie_wartosc.grid(row=1, column=1)

    label_szczegoly_pracownika_nazwisko = Label(ramka_szczegoly_pracownika, text='Nazwisko: ')
    label_szczegoly_pracownika_nazwisko.grid(row=1, column=2)

    label_szczegoly_pracownika_nazwisko_wartosc = Label(ramka_szczegoly_pracownika, text='....')
    label_szczegoly_pracownika_nazwisko_wartosc.grid(row=1, column=3)

    label_szczegoly_pracownika_wiek = Label(ramka_szczegoly_pracownika, text='Wiek: ')
    label_szczegoly_pracownika_wiek.grid(row=1, column=4)

    label_szczegoly_pracownika_wiek_wartosc = Label(ramka_szczegoly_pracownika, text='....')
    label_szczegoly_pracownika_wiek_wartosc.grid(row=1, column=5)
    
    label_szczegoly_pracownika_nazwa_myjni = Label(ramka_szczegoly_pracownika, text='Nazwa myjni: ')
    label_szczegoly_pracownika_nazwa_myjni.grid(row=1, column=6)

    label_szczegoly_pracownika_nazwa_myjni_wartosc = Label(ramka_szczegoly_pracownika, text='....')
    label_szczegoly_pracownika_nazwa_myjni_wartosc.grid(row=1, column=7)
    
    label_szczegoly_pracownika_miasto = Label(ramka_szczegoly_pracownika, text='Miasto: ')
    label_szczegoly_pracownika_miasto.grid(row=1, column=8)

    label_szczegoly_pracownika_miasto_wartosc = Label(ramka_szczegoly_pracownika, text='....')
    label_szczegoly_pracownika_miasto_wartosc.grid(row=1, column=9)

    entry_pracownika_imie = Entry(ramka_formularz_pracownikow)
    entry_pracownika_imie.grid(row=1, column=1)
    entry_pracownika_nazwisko = Entry(ramka_formularz_pracownikow)
    entry_pracownika_nazwisko.grid(row=2, column=1)
    entry_pracownika_wiek = Entry(ramka_formularz_pracownikow)
    entry_pracownika_wiek.grid(row=3, column=1)
    entry_pracownika_miasto = Entry(ramka_formularz_pracownikow)
    entry_pracownika_miasto.grid(row=4, column=1)
    entry_pracownika_nazwa_myjni = Entry(ramka_formularz_pracownikow)
    entry_pracownika_nazwa_myjni.grid(row=5, column=1)

    map_widget_pracownika = tkintermapview.TkinterMapView(ramka_mapa_pracownicy, width=1200, height=400, corner_radius=0)
    map_widget_pracownika.grid(row=0, column=0, columnspan=2)
    map_widget_pracownika.set_position(52.23, 21.00)
    map_widget_pracownika.set_zoom(6)


