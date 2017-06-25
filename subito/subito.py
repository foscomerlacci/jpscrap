#! /usr/bin/python3

__author__ = 'utente'

from bs4 import BeautifulSoup
import urllib.request
import sqlite3
import time
from datetime import date, datetime

def main():

    links = []                                              # creo le liste vuote
    descrizione = []                                        #
    data = []                                               #
    luogo = []
    inserzionista = []                                                 #
    conn = sqlite3.connect('test.sqlite')                   # creo la connessione al db sqlite
    c = conn.cursor()                                       # creo il puntatore
    inizio = time.time()                                    # creo il momento 0 per calcolare il tempo di esecuzione

    def getInserzionista(url):
        html_page = urllib.request.urlopen(url)     # carico la pagina in html_page
        soup = BeautifulSoup(html_page, "lxml")     # creo il SOUP attraverso il parser lxml
        inserz = soup.select('.author.btn_author_reply')[0].get_text()
        # print(inserz)
        inserzionista.append(inserz)


    def getLinks(url):
        html_page = urllib.request.urlopen(url)     # carico la pagina in html_page
        soup = BeautifulSoup(html_page, "lxml")     # creo il SOUP attraverso il parser lxml
        collegamenti = soup.select("h2 a")          # filtro il SOUP alla ricerca dei collegamenti
        date = soup.select("time")                  # filtro il SOUP alla ricerca della data

        for collegamento in collegamenti:
            links.append(collegamento.attrs["href"])
            getInserzionista(collegamento.attrs["href"])

        for row in soup.findAll('div',{'class' : 'item_list_section item_description'}):  # accodo alla lista data il risultato del ciclo di filtro su link
            descrizione.append(str(list(row.contents)[1].get_text()).strip())             # tolgo gli spazi iniziali

        for x in date:
            data.append(x.attrs["datetime"])
        for ins in soup.findAll('span', {'class':'item_location'}):   # accodo alla lista data il risultato del ciclo di filtro
            luogo.append(str(ins.get_text()))

    for x in range(1, 2):
        getLinks("http://www.subito.it/annunci-lazio/vendita/offerte-lavoro/roma/roma/?q=sistemista&o="+ str(x))

    # print(data)
    # print(links)
    # print(luogo)
    # print(descrizione)
    # print(inserzionista)

    ris = zip(reversed(data),  reversed(links), reversed(luogo), reversed(descrizione), reversed(inserzionista),)

    for r in ris:
        c.execute('''SELECT link FROM annunci''')
        elenco = str(c.fetchall())
        t_inseriti = 0
        if r[1] in elenco:                  # qui verifico che l'annuncio non sia gia' stato salvato
            print("record gia' inserito")
        else:

            c.execute('''INSERT INTO annunci(data, link, luogo, descrizione, inserzionista, timestamp) VALUES(?,?,?,?,?,?)''',(r[0], r[1], r[2], r[3], r[4], str(datetime.now())))
            print(str(r[0])+" -- "+ r[1]+" -- "+ str(r[2])+" -- "+ str(r[3])+"--"+ str(r[4])+"--")
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
    print("evvivaaaaaaaaaaaaaaaaaaaa!!!!!!!!")
if __name__ == '__main__': main()