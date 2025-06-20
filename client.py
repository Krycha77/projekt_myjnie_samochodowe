from tkinter import *
from tkinter.ttk import Combobox

from tkcalendar import DateEntry

from utils import city_not_found_message, are_params_filled
from data import clients, get_carwashes
import tkintermapview

from tkinter import ttk


class Client:
    def __init__(self, first_name, last_name, carwash_name, city, visit_date, widget):
        self.first_name = first_name
        self.last_name = last_name
        self.carwash_name = carwash_name
        self.city = city
        self.visit_date = visit_date
        self.coordinates = self.get_coordinates()
        self.marker = widget.set_marker(self.coordinates[0], self.coordinates[1],
                                        text=f'{self.first_name} {self.last_name}')

    # FUNKCJA WEWNĄTRZ KLASY TO METODA
    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        adres_url: str = f'https://pl.wikipedia.org/wiki/{self.city}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')

        if len(response_html.select('.latitude')) < 2:
            city_not_found_message()
            return

        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.')),
        ]


def configure_client_gui(tab3: ttk.Frame) -> None:
    def add_client() -> None:
        first_name = entry_klienta_imie.get()
        last_name = entry_klienta_nazwisko.get()
        carwash_name = entry_klienta_nazwa_myjni.get()
        city = entry_klienta_miasto.get()
        visit_date = entry_klienta_data_wizyty.get()
        if not are_params_filled(first_name, last_name, carwash_name, city):
            return

        client = Client(first_name=first_name, last_name=last_name, carwash_name=carwash_name, city=city, visit_date=visit_date,
                            widget=map_widget_klienta)
        clients.append(client)

        entry_klienta_imie.delete(0, END)
        entry_klienta_nazwisko.delete(0, END)
        entry_klienta_nazwa_myjni.delete(0, END)
        entry_klienta_miasto.delete(0, END)
        entry_klienta_data_wizyty.delete(0, END)

        entry_klienta_imie.focus()
        show_clients()

    def show_clients():
        listbox_lista_klientow.delete(0, END)
        for idx, client in enumerate(clients):
            listbox_lista_klientow.insert(idx,
                                             f'{idx + 1}. {client.first_name} {client.last_name} {client.carwash_name} {client.city} {client.visit_date}')

    def remove_client():
        i = listbox_lista_klientow.index(ACTIVE)
        print(i)
        clients[i].marker.delete()
        clients.pop(i)
        show_clients()

    def edit_client():
        i = listbox_lista_klientow.index(ACTIVE)
        first_name = clients[i].first_name
        last_name = clients[i].last_name
        carwash_name = clients[i].carwash_name
        city = clients[i].city
        visit_date = clients[i].visit_date

        entry_klienta_imie.insert(0, first_name)
        entry_klienta_nazwisko.insert(0, last_name)
        entry_klienta_nazwa_myjni.insert(0, carwash_name)
        entry_klienta_miasto.insert(0, city)
        entry_klienta_data_wizyty.set_date(visit_date)

        button_dodaj_klienta.config(text='Zapisz', command=lambda: update_client(i))

    def update_client(i):
        first_name = entry_klienta_imie.get()
        last_name = entry_klienta_nazwisko.get()
        carwash_name = entry_klienta_nazwa_myjni.get()
        city = entry_klienta_miasto.get()
        visit_date = entry_klienta_data_wizyty.get()
        if not are_params_filled(first_name, last_name, carwash_name, city):
            return

        clients[i].first_name = first_name
        clients[i].last_name = last_name
        clients[i].carwash_name = carwash_name
        clients[i].city = city
        clients[i].visit_date = visit_date

        clients[i].coordinates = clients[i].get_coordinates()
        clients[i].marker.delete()
        clients[i].marker = map_widget_klienta.set_marker(clients[i].coordinates[0], clients[i].coordinates[1],
                                                               text=f'{clients[i].first_name} {clients[i].last_name}')

        show_clients()
        button_dodaj_klienta.config(text='Dodaj', command=add_client)

        entry_klienta_imie.delete(0, END)
        entry_klienta_nazwisko.delete(0, END)
        entry_klienta_nazwa_myjni.delete(0, END)
        entry_klienta_miasto.delete(0, END)
        entry_klienta_data_wizyty.delete(0, END)

        entry_klienta_imie.focus()

    def show_client_details():
        i = listbox_lista_klientow.index(ACTIVE)
        label_szczegoly_klienta_imie_wartosc.config(text=clients[i].first_name)
        label_szczegoly_klienta_nazwisko_wartosc.config(text=clients[i].last_name)
        label_szczegoly_klienta_nazwa_myjni_wartosc.config(text=clients[i].carwash_name)
        label_szczegoly_klienta_miasto_wartosc.config(text=clients[i].city)
        label_szczegoly_klienta_data_wizyty_wartosc.config(text=clients[i].visit_date)

        map_widget_klienta.set_zoom(15)
        map_widget_klienta.set_position(clients[i].coordinates[0], clients[i].coordinates[1])

    def refresh_carwash_list():
        entry_klienta_nazwa_myjni['values'] = get_carwashes()

    ramka_lista_klientow = Frame(tab3)
    ramka_formularz_klientow = Frame(tab3)
    ramka_szczegoly_klienta = Frame(tab3)
    ramka_mapa_klienci = Frame(tab3)

    ramka_lista_klientow.grid(row=0, column=0)
    ramka_formularz_klientow.grid(row=0, column=1)
    ramka_szczegoly_klienta.grid(row=2, column=0, columnspan=2)
    ramka_mapa_klienci.grid(row=3, column=0, columnspan=2)

    button_dodaj_klienta = Button(ramka_formularz_klientow, text='Dodaj', command=add_client)
    button_dodaj_klienta.grid(row=6, column=0, columnspan=2)

    label_lista_klienta = Label(ramka_lista_klientow, text='Lista pracowników:')
    label_lista_klienta.grid(row=0, column=0)

    listbox_lista_klientow = Listbox(ramka_lista_klientow, width=50, height=10)
    listbox_lista_klientow.grid(row=1, column=0, columnspan=3)

    button_pokaz_klienta = Button(ramka_lista_klientow, text='Pokaż szczegóły', command=show_client_details)
    button_pokaz_klienta.grid(row=2, column=0)
    button_usun_klienta = Button(ramka_lista_klientow, text='Usuń', command=remove_client)
    button_usun_klienta.grid(row=2, column=1)
    button_edytuj_klienta = Button(ramka_lista_klientow, text='Edytuj', command=edit_client)
    button_edytuj_klienta.grid(row=2, column=2)

    label_formularz_pracownik = Label(ramka_formularz_klientow, text='Formularz:')
    label_formularz_pracownik.grid(row=0, column=0)

    label_szczegoly_klienta_imie = Label(ramka_formularz_klientow, text='Imię:')
    label_szczegoly_klienta_imie.grid(row=1, column=0, sticky=W)

    label_szczegoly_klienta_nazwisko = Label(ramka_formularz_klientow, text='Nazwisko:')
    label_szczegoly_klienta_nazwisko.grid(row=2, column=0, sticky=W)

    label_szczegoly_klienta_miasto = Label(ramka_formularz_klientow, text='Miasto:')
    label_szczegoly_klienta_miasto.grid(row=3, column=0, sticky=W)

    label_szczegoly_klienta_myjnia = Label(ramka_formularz_klientow, text='Nazwa myjni:')
    label_szczegoly_klienta_myjnia.grid(row=4, column=0, sticky=W)

    label_szczegoly_klienta_data_wizyty = Label(ramka_formularz_klientow, text='Data wizyty:')
    label_szczegoly_klienta_data_wizyty.grid(row=5, column=0, sticky=W)

    # Ramka_szczegoly_klienta
    label_pokaz_szczegoly_klienta = Label(ramka_szczegoly_klienta, text='Szczegóły klienta:')
    label_pokaz_szczegoly_klienta.grid(row=0, column=0)

    label_szczegoly_klienta_imie = Label(ramka_szczegoly_klienta, text='Imię: ')
    label_szczegoly_klienta_imie.grid(row=1, column=0, sticky=E)

    label_szczegoly_klienta_imie_wartosc = Label(ramka_szczegoly_klienta, text='....')
    label_szczegoly_klienta_imie_wartosc.grid(row=1, column=1)

    label_szczegoly_klienta_nazwisko = Label(ramka_szczegoly_klienta, text='Nazwisko: ')
    label_szczegoly_klienta_nazwisko.grid(row=1, column=2)

    label_szczegoly_klienta_nazwisko_wartosc = Label(ramka_szczegoly_klienta, text='....')
    label_szczegoly_klienta_nazwisko_wartosc.grid(row=1, column=3)

    label_szczegoly_klienta_nazwa_myjni = Label(ramka_szczegoly_klienta, text='Nazwa myjni: ')
    label_szczegoly_klienta_nazwa_myjni.grid(row=1, column=4)

    label_szczegoly_klienta_nazwa_myjni_wartosc = Label(ramka_szczegoly_klienta, text='....')
    label_szczegoly_klienta_nazwa_myjni_wartosc.grid(row=1, column=5)

    label_szczegoly_klienta_miasto = Label(ramka_szczegoly_klienta, text='Miasto: ')
    label_szczegoly_klienta_miasto.grid(row=1, column=6)

    label_szczegoly_klienta_miasto_wartosc = Label(ramka_szczegoly_klienta, text='....')
    label_szczegoly_klienta_miasto_wartosc.grid(row=1, column=7)

    label_szczegoly_klienta_data_wizyty = Label(ramka_szczegoly_klienta, text='Data wizyty: ')
    label_szczegoly_klienta_data_wizyty.grid(row=1, column=8)

    label_szczegoly_klienta_data_wizyty_wartosc = Label(ramka_szczegoly_klienta, text='....')
    label_szczegoly_klienta_data_wizyty_wartosc.grid(row=1, column=9)

    entry_klienta_imie = Entry(ramka_formularz_klientow)
    entry_klienta_imie.grid(row=1, column=1)
    entry_klienta_nazwisko = Entry(ramka_formularz_klientow)
    entry_klienta_nazwisko.grid(row=2, column=1)
    entry_klienta_miasto = Entry(ramka_formularz_klientow)
    entry_klienta_miasto.grid(row=3, column=1)
    entry_klienta_nazwa_myjni = Combobox(ramka_formularz_klientow, postcommand=refresh_carwash_list)
    entry_klienta_nazwa_myjni.grid(row=4, column=1)
    entry_klienta_data_wizyty = DateEntry(ramka_formularz_klientow)
    entry_klienta_data_wizyty.grid(row=5, column=1)

    map_widget_klienta = tkintermapview.TkinterMapView(ramka_mapa_klienci, width=1400, height=600,
                                                          corner_radius=0)
    map_widget_klienta.grid(row=0, column=0, columnspan=2)
    map_widget_klienta.set_position(52.23, 21.00)
    map_widget_klienta.set_zoom(6)

    refresh_carwash_list()

