#! /usr/bin/python3

__author__ = 'utente'

from bs4 import BeautifulSoup
import urllib.request
import re
import sqlite3
import time
from mail_sender import sendemail
from datetime import date, datetime
from time import localtime, strftime

links = []  # creo le liste vuote
descrizione = []  #
data = []  #
inserzionista = []  #
luogo = []  #
lista = ("sistemista","informatico",)




def getLinks(url):  # la funzione che accetta un link e rende popolate le liste links, data, inserzionista, luogo

    html_page = urllib.request.urlopen(url)  # carico la pagina in html_page
    soup = BeautifulSoup(html_page, "lxml")  # creo il soup attraverso il parser lxml

    for link in soup.select("tr a", ):  # accodo alla lista links il risultato del ciclo di filtro che cerca i links
        links.append(link.get('href'))  # aggiungo l'indirizzo alla lista links
        descrizione.append(link.get_text())

    for record in soup.find_all('tr'):  # accodo alla lista data il risultato del ciclo di filtro
        data.append(record.contents[1].get_text())
        # data.append(record.contents[1].get('datetime'))
        inserzionista.append(record.contents[3].get_text())  # accodo alla lista inserzionista
        luogo.append(record.contents[7].get_text())  # accodo alla lista luogo


def main():

    conn = sqlite3.connect('test.sqlite')  # creo la connessione al db sqlite
    c = conn.cursor()  # creo il puntatore della connessione
    c.execute('PRAGMA journal_mode=wal')            # imposto il Write-Ahead Logging
    inizio = time.time()  # creo il momento 0 per calcolare il tempo di esecuzione
    t_inseriti = 0

    for t in lista:

        for x in range(1, 2):  # ciclo 2 pagine di annunci dentro la funzione che che ne estrae annunci
            getLinks("http://www.iprogrammatori.it/lavoro/s/" + t + "-roma/lazio/roma?page=" + str(x))  #

        ris = zip(reversed(data), reversed(descrizione), reversed(links), reversed(inserzionista),
                  reversed(luogo))  # qui si invertono le liste e se ne fa un unico thread fatto a fette da un ciclo

        c.execute('''SELECT link FROM annunci;''')
        elenco = str(c.fetchall())
        #conn.close()
        # if ris == 0:
        #     print("ciao")
        for r in ris:  # qui ciclo le fette salvandole sul db e scrivendolo a schermo

            # print(r)

            if r[2] in elenco:  # qui verifico che l'annuncio non sia gia' stato salvato
                print("record gia' inserito")
                # print(type(elenco),type(r[2]))
            else:
                c.execute('''INSERT INTO annunci(data, descrizione, link, inserzionista, luogo, timestamp) VALUES(?,?,?,?,?,?)''',(r[0], r[1], r[2], r[3], r[4], str(datetime.now())))
                #conn.close()
                print(r[0] + " -- " + r[1] + " -- " + str(r[2]) + " -- " + r[3] + " -- " + r[4])

                sendemail(message=(r[0] + " -- " + r[1] + " -- " + str(r[2]) + " -- " + r[3] + " -- " + r[4]), subject=('Cercasi '+ t))


                # print(r)
                # print("evvivaaaaaaaaaaaaaaaaaaaa!!!!!!!!")
                t_inseriti = t_inseriti + 1
                c.execute('''SELECT link FROM annunci;''')
                elenco = str(c.fetchall())
                # print(type(elenco), type(r[2]))
                # print(elenco)

        conn.commit()
    conn.close()
    print("\n")

    fine = time.time()  # creo il momento 1
    if t_inseriti == 1:
        x = "o"
    else:
        x = " "
    print("Il job ha impiegato " + str(round((fine - inizio), 2)) + " secondi per inserire " + str(
        t_inseriti) + " annunci" + str(x))  # stampo il tempo di esecuzione del job di web scraping
    print(strftime("%a, %d %b %Y %H:%M:%S", localtime()) + " evvivaaaaaaaaaaaaaaaaaaaa!!!!!!!!")
    print("\n")


if __name__ == '__main__': main()
