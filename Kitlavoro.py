#! /usr/bin/python3

__author__ = 'utente'

from bs4 import BeautifulSoup
import urllib.request
import re
import sqlite3
import time
from datetime import date, datetime



def main():
    links = []  # creo le liste vuote
    descrizione = []  #
    data = []  #
    inserzionista = []  #
    luogo = []  #
    conn = sqlite3.connect('test.sqlite')  # creo la connessione al db sqlite
    c = conn.cursor()  # creo il puntatore della connessione
    inizio = time.time()  # creo il momento 0 per calcolare il tempo di esecuzione
    rx = re.compile("^http://www.kitlavoro.it/lavoro")  # creo la reg exp per filtrare i links giusti

    def getLinks(url):    # la funzione che accetta un link e rende popolate le liste links, data, inserzionista, luogo

        html_page = urllib.request.urlopen(url)  # carico la pagina in html_page
        soup = BeautifulSoup(html_page, "lxml")  # creo il soup attraverso il parser lxml

        for link in soup.findAll('a', attrs={'href': rx}):  # accodo alla lista links il risultato del ciclo di filtro che cerca i links contenenti rx
            descrizione.append(link.get('title'))  # aggiungo il titolo alla lista descrizione
            links.append(link.get('href'))  # aggiungo l'indirizzo alla lista links

        for record in soup.findAll('span',{'class': 'date'}):  # accodo alla lista data il risultato del ciclo di filtro
            data.append(record.get_text())  # accodo alla lista data

        for ins in soup.findAll('span',{'class': 'company_name'}):  # accodo alla lista data il risultato del ciclo di filtro
            inserzionista.append(str(ins.get_text()).splitlines()[1][3:-3])  # accodo alla lista inserzionista
            luogo.append(str(ins.get_text()).splitlines()[2])  # accodo alla lista luogo dopo aver scelto il 3° split del text di ins

    for x in range(1, 3):                      # ciclo 2 pagine di annunci dentro la funzione che che ne estrae annunci
        getLinks("http://www.kitlavoro.it/search/roma/?p=" + str(x))  #

    ris = zip(reversed(data), reversed(descrizione), reversed(links), reversed(inserzionista), reversed(luogo))  # qui si invertono le liste e se ne fa un unico thread fatto a fette da un ciclo

    c.execute('''SELECT link FROM annunci;''')
    elenco = c.fetchall()
    t_inseriti = 0
    for r in ris:  # qui ciclo le fette salvandole sul db e scrivendolo a schermo
        # print(elenco)
        # print(r[2])
        # print(type(elenco))
        # print(type(r[2]))
        # print(tuple(r[2]))
        # x = r[2]
        c.execute('''SELECT link FROM annunci''')
        elenco = str(c.fetchall())
        # print(elenco)
        # print(type(elenco[0]))

        # if "http://www.kitlavoro.it/lavoro/2683242/promozione-eventi_roma-roma/" in elenco: print("diooooooooooooooooboiaaaaaaa")
        # for l in elenco:
        #     print(l)
        #     if l == r[2]:
        #         print("presente")
        #     else:
        #         print("non presente")
            # print(elenco)
            # print(r[2])
        if r[2] in elenco:                  # qui verifico che l'annuncio non sia gia' stato salvato
            print("record gia' inserito")
        else:
            c.execute('''INSERT INTO annunci(data, descrizione, link, inserzionista, luogo, timestamp) VALUES(?,?,?,?,?,?)''',(r[0], r[1], r[2], r[3], r[4], str(datetime.now())))
            # print(r[0] + " -- " + r[1] + " -- " + str(r[2]) + " -- " + r[3] + " -- " + r[4])
            # print(r)
            print("evvivaaaaaaaaaaaaaaaaaaaa!!!!!!!!")
            t_inseriti = t_inseriti + 1

    conn.commit()
    conn.close()

    print("\n")
    fine = time.time()  # creo il momento 1
    if t_inseriti == 1:
        x = "o"
    else:
        x = " "
    print("Il job ha impiegato " + str(round((fine - inizio), 2)) + " secondi per inserire " + str(t_inseriti) + " annunci" + str(x) )  # stampo il tempo di esecuzione del job di web scraping


if __name__ == '__main__': main()
