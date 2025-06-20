from tkinter import *
from utils import city_not_found_message

import tkintermapview

from tkinter import ttk

carwashes: list = []


class Carwash:
    def __init__(self, name, owner, location, widget):
        self.name = name
        self.owner = owner
        self.location = location
        self.coordinates = self.get_coordinates()
        self.marker = widget.set_marker(self.coordinates[0], self.coordinates[1],
                                            text=f'{self.name} {self.owner}')

    # FUNKCJA WEWNĄTRZ KLASY TO METODA
    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        adres_url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')

        if len(response_html.select('.latitude'))<2:
            city_not_found_message()
            return

        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.')),
        ]



def configure_carwash_gui(tab1: ttk.Frame) -> None:
    def add_carwash() -> None:
        name = entry_myjnia_nazwa.get()
        owner = entry_myjnia_wlasciciel.get()
        location = entry_myjnia_miejscowosc.get()

        carwash = Carwash(name=name, owner=owner, location=location, widget=map_widget_myjnie)
        carwashes.append(carwash)

        print(carwashes)

        entry_myjnia_nazwa.delete(0, END)
        entry_myjnia_wlasciciel.delete(0, END)
        entry_myjnia_miejscowosc.delete(0, END)

        entry_myjnia_nazwa.focus()
        show_carwashes()

    def show_carwashes():
        listbox_lista_myjni.delete(0, END)
        for idx, carwash in enumerate(carwashes):
            listbox_lista_myjni.insert(idx, f'{idx + 1}. {carwash.name} {carwash.owner}')

    def remove_carwash():
        i = listbox_lista_myjni.index(ACTIVE)
        print(i)
        carwashes[i].marker.delete()
        carwashes.pop(i)
        show_carwashes()

    def edit_carwash():
        i = listbox_lista_myjni.index(ACTIVE)
        name = carwashes[i].name
        owner = carwashes[i].owner
        location = carwashes[i].location

        entry_myjnia_nazwa.insert(0, name)
        entry_myjnia_wlasciciel.insert(0, owner)
        entry_myjnia_miejscowosc.insert(0, location)

        button_dodaj_myjnie.config(text='Zapisz', command=lambda: update_carwash(i))

    def update_carwash(i):
        name = entry_myjnia_nazwa.get()
        owner = entry_myjnia_wlasciciel.get()
        location = entry_myjnia_miejscowosc.get()

        carwashes[i].name = name
        carwashes[i].owner = owner
        carwashes[i].location = location

        carwashes[i].coordinates = carwashes[i].get_coordinates()
        carwashes[i].marker.delete()
        carwashes[i].marker = map_widget_myjnie.set_marker(carwashes[i].coordinates[0], carwashes[i].coordinates[1],
                                                           text=f'{carwashes[i].name} {carwashes[i].owner}')

        show_carwashes()
        button_dodaj_myjnie.config(text='Dodaj', command=add_carwash)

        entry_myjnia_nazwa.delete(0, END)
        entry_myjnia_wlasciciel.delete(0, END)
        entry_myjnia_miejscowosc.delete(0, END)
        entry_myjnia_miejscowosc.delete(0, END)

        entry_myjnia_nazwa.focus()

    def show_carwash_details():
        i = listbox_lista_myjni.index(ACTIVE)
        label_szczegoly_myjni_nazwa_wartosc.config(text=carwashes[i].name)
        label_szczegoly_myjni_wlasciciel_wartosc.config(text=carwashes[i].owner)
        label_szczegoly_myjni_miejscowosc_wartosc.config(text=carwashes[i].location)

        map_widget_myjnie.set_zoom(15)
        map_widget_myjnie.set_position(carwashes[i].coordinates[0], carwashes[i].coordinates[1])



    ramka_lista_myjni = Frame(tab1)
    ramka_formularz_myjni = Frame(tab1)
    ramka_szczegoly_myjni = Frame(tab1)
    ramka_mapa_myjnie = Frame(tab1)

    ramka_lista_myjni.grid(row=0, column=0)
    ramka_formularz_myjni.grid(row=0, column=1)
    ramka_szczegoly_myjni.grid(row=2, column=0, columnspan=2)
    ramka_mapa_myjnie.grid(row=3, column=0, columnspan=2)

    button_dodaj_myjnie = Button(ramka_formularz_myjni, text='Dodaj', command=add_carwash)
    button_dodaj_myjnie.grid(row=5, column=0, columnspan=2)

    # ramka_lista_myjni
    label_lista_myjni = Label(ramka_lista_myjni, text='Lista użytkowników:')
    label_lista_myjni.grid(row=0, column=0)

    listbox_lista_myjni = Listbox(ramka_lista_myjni, width=50, height=10)
    listbox_lista_myjni.grid(row=1, column=0, columnspan=3)

    button_pokaz_myjnie = Button(ramka_lista_myjni, text='Pokaż szczegóły', command=show_carwash_details)
    button_pokaz_myjnie.grid(row=2, column=0)
    button_usun_myjnie = Button(ramka_lista_myjni, text='Usuń', command=remove_carwash)
    button_usun_myjnie.grid(row=2, column=1)
    button_edytuj_myjnie = Button(ramka_lista_myjni, text='Edytuj', command=edit_carwash)
    button_edytuj_myjnie.grid(row=2, column=2)

    label_formularz_myjnia = Label(ramka_formularz_myjni, text='Formularz:')
    label_formularz_myjnia.grid(row=0, column=0)

    label_szczegoly_myjni_nazwa = Label(ramka_formularz_myjni, text='Nazwa:')
    label_szczegoly_myjni_nazwa.grid(row=1, column=0, sticky=W)

    label_szczegoly_myjni_wlasciciel = Label(ramka_formularz_myjni, text='Wlaściciel:')
    label_szczegoly_myjni_wlasciciel.grid(row=2, column=0, sticky=W)

    label_szczegoly_myjni_miejscowosc = Label(ramka_formularz_myjni, text='Miejscowość:')
    label_szczegoly_myjni_miejscowosc.grid(row=3, column=0, sticky=W)

    # Ramka_szczegoly_myjni
    label_pokaz_szczegoly_myjni = Label(ramka_szczegoly_myjni, text='Szczegóły myjni:')
    label_pokaz_szczegoly_myjni.grid(row=0, column=0)

    label_szczegoly_myjni_nazwa = Label(ramka_szczegoly_myjni, text='Nazwa: ')
    label_szczegoly_myjni_nazwa.grid(row=1, column=0, sticky=E)

    label_szczegoly_myjni_nazwa_wartosc = Label(ramka_szczegoly_myjni, text='....')
    label_szczegoly_myjni_nazwa_wartosc.grid(row=1, column=1)

    label_szczegoly_myjni_wlasciciel = Label(ramka_szczegoly_myjni, text='Właściciel: ')
    label_szczegoly_myjni_wlasciciel.grid(row=1, column=2)

    label_szczegoly_myjni_wlasciciel_wartosc = Label(ramka_szczegoly_myjni, text='....')
    label_szczegoly_myjni_wlasciciel_wartosc.grid(row=1, column=3)

    label_szczegoly_myjni_miejscowosc = Label(ramka_szczegoly_myjni, text='Miescowość: ')
    label_szczegoly_myjni_miejscowosc.grid(row=1, column=4)

    label_szczegoly_myjni_miejscowosc_wartosc = Label(ramka_szczegoly_myjni, text='....')
    label_szczegoly_myjni_miejscowosc_wartosc.grid(row=1, column=5)

    entry_myjnia_nazwa = Entry(ramka_formularz_myjni)
    entry_myjnia_nazwa.grid(row=1, column=1)
    entry_myjnia_wlasciciel = Entry(ramka_formularz_myjni)
    entry_myjnia_wlasciciel.grid(row=2, column=1)
    entry_myjnia_miejscowosc = Entry(ramka_formularz_myjni)
    entry_myjnia_miejscowosc.grid(row=3, column=1)

    map_widget_myjnie = tkintermapview.TkinterMapView(ramka_mapa_myjnie, width=1200, height=400, corner_radius=0)
    map_widget_myjnie.grid(row=0, column=0, columnspan=2)
    map_widget_myjnie.set_position(52.23, 21.00)
    map_widget_myjnie.set_zoom(6)


