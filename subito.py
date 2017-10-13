#! /usr/bin/python3

__author__ = 'utente'

from bs4 import BeautifulSoup
import urllib.request
import sqlite3
import time
from time import localtime, strftime
from datetime import date, datetime
from mail_sender import sendemail

links = []                                              # creo le liste vuote
descrizione = []                                        #
data = []                                               #
luogo = []
inserzionista = []
lista = ("help+desk","sistemista","informatico",)                                           #


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
            getInserzionista(collegamento.attrs["href"])        # richiamo la funzione che apre il link e continua a cercare l'inserzionista

        for row in soup.findAll('div',{'class' : 'item_list_section item_description'}):  # accodo alla lista data il risultato del ciclo di filtro su link
            descrizione.append(str(list(row.contents)[1].get_text()).strip())             # tolgo gli spazi iniziali

        for x in date:
            data.append(x.attrs["datetime"])
        for ins in soup.findAll('span', {'class':'item_location'}):   # accodo alla lista data il risultato del ciclo di filtro
            luogo.append(str(ins.get_text()))



def main():


    conn = sqlite3.connect('test.sqlite')                   # creo la connessione al db sqlite
    c = conn.cursor()                                       # creo il puntatore
    c.execute('PRAGMA journal_mode=wal')                    # imposto il Write-Ahead Logging
    inizio = time.time()                                    # creo il momento 0 per calcolare il tempo di esecuzione
    t_inseriti = 0


    for t in lista:

        for x in range(1, 2):
            # getLinks("http://www.subito.it/annunci-lazio/vendita/offerte-lavoro/roma/roma/?q=sistemista&o="+ str(x))
            getLinks("http://www.subito.it/annunci-lazio/vendita/offerte-lavoro/roma/roma/?q=" + t + "&o="+ str(x))

        # print(data)
        # print(links)
        # print(luogo)
        # print(descrizione)
        # print(inserzionista)

        ris = zip(reversed(data),  reversed(descrizione), reversed(links), reversed(inserzionista), reversed(luogo),)

        c.execute('''SELECT link FROM annunci;''')
        elenco = str(c.fetchall())
        #conn.close()


        for r in ris:  # qui ciclo le fette salvandole sul db e scrivendolo a schermo

            # print(r)
            # print(elenco)
            if r[2] in elenco:                  # qui verifico che l'annuncio non sia gia' stato salvato
                print("record gia' inserito")
                # print(type(elenco),type(r[2]))
                # print(r[2])
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
    print("Il job ha impiegato " + str(round((fine - inizio), 2)) + " secondi per inserire " + str(t_inseriti) + " annunci" + str(x) )  # stampo il tempo di esecuzione del job di web scraping
    print(strftime("%a, %d %b %Y %H:%M:%S", localtime()) + " evvivaaaaaaaaaaaaaaaaaaaa!!!!!!!!")
    print("\n")

if __name__ == '__main__': main()
