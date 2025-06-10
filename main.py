from tkinter import *
import tkintermapview

root = Tk()
root.geometry("1400x800")
root.title('CarWash Manager')


ramka_lista_myjni = Frame(root)
ramka_formularz_myjni = Frame(root)
ramka_formularz_pracownicy = Frame(root)
ramka_formularz_klienci = Frame(root)
ramka_szczegoly = Frame(root)
ramka_mapa = Frame(root)


ramka_lista_myjni.grid(row=0, column=0)
ramka_formularz_myjni.grid(row=0, column=1)
ramka_formularz_pracownicy.grid(row=1, column=0)
ramka_formularz_klienci.grid(row=1, column=1)
ramka_szczegoly.grid(row=2, column=0, columnspan=2)
ramka_mapa.grid(row=3, column=0, columnspan=2)



Label(ramka_formularz_myjni, text='Dodaj myjnię:').grid(row=0, column=0, columnspan=2)
Label(ramka_formularz_myjni, text='Nazwa:').grid(row=1, column=0, sticky=W)
Label(ramka_formularz_myjni, text='Właściciel:').grid(row=2, column=0, sticky=W)
Label(ramka_formularz_myjni, text='Miasto:').grid(row=3, column=0, sticky=W)


Entry(ramka_formularz_myjni).grid(row=1, column=1)
Entry(ramka_formularz_myjni).grid(row=2, column=1)
Entry(ramka_formularz_myjni).grid(row=3, column=1)


Button(ramka_formularz_myjni, text='Dodaj myjnię').grid(row=6, column=0, columnspan=2)


Label(ramka_formularz_pracownicy, text='Dodaj pracownika:').grid(row=0, column=0, columnspan=2)
Label(ramka_formularz_pracownicy, text='Imię:').grid(row=1, column=0, sticky=W)
Label(ramka_formularz_pracownicy, text='Nazwisko:').grid(row=2, column=0, sticky=W)
Label(ramka_formularz_pracownicy, text='Myjnia (nazwa):').grid(row=3, column=0, sticky=W)


Entry(ramka_formularz_pracownicy).grid(row=1, column=1)
Entry(ramka_formularz_pracownicy).grid(row=2, column=1)
Entry(ramka_formularz_pracownicy).grid(row=3, column=1)

Button(ramka_formularz_pracownicy, text='Dodaj pracownika').grid(row=6, column=0, columnspan=2)


Label(ramka_formularz_klienci, text='Dodaj klienta:').grid(row=0, column=0, columnspan=2)
Label(ramka_formularz_klienci, text='Imię:').grid(row=1, column=0, sticky=W)
Label(ramka_formularz_klienci, text='Nazwisko:').grid(row=2, column=0, sticky=W)
Label(ramka_formularz_klienci, text='Myjnia (nazwa):').grid(row=3, column=0, sticky=W)


Entry(ramka_formularz_klienci).grid(row=1, column=1)
Entry(ramka_formularz_klienci).grid(row=2, column=1)
Entry(ramka_formularz_klienci).grid(row=3, column=1)


Button(ramka_formularz_klienci, text='Dodaj klienta').grid(row=6, column=0, columnspan=2)


map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=400, corner_radius=0)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(6)

root.mainloop()