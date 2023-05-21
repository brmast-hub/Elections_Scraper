"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie
author: Martin Brejcha
email: brmast@seznam.cz
discord: Martin B.#5188
"""

import requests
import bs4
import sys
import csv
from bs4 import BeautifulSoup

def seznam_uzemnich_celku(vstupni_data): 
# vytvoří seznam všech uzemních celků, které je možno scrapovat   
    seznam_okrsku = list()
    pocet = 0
    while pocet < len(volebni_soup):
        mesto = volebni_soup[pocet].text
        pocet += 1
        if "CZ0" not in mesto and mesto != "X" and mesto != "N":
            seznam_okrsku.append(mesto)
    return seznam_okrsku
    
def kontrola_vstupnich_hodnot(vstupni_argumenty, seznam_okrsku, zadane_mesto):
# kontrola vstupních argumentů
    # kontrola počtu argumentů
    if len(sys.argv) != 3: 
        print("zadej 3 argumenty")
        return False
    # porovnání 2. argumentu a seznamu uzemních celků
    seznam_uzemnich_celku(seznam_okrsku)
    if zadane_mesto not in seznam_okrsku: 
        print("\nChybně zadaný volební okrsek !!!\nk dispozici jsou jen níže uvedené volební okrsky\nmezery v nazvu měst nahraďte při zadávání podtržítkem")
        print(60*"-")
        print(seznam_okrsku)
        return False
    # kontrola 3. argumentu - aspoň jedna pozice a koncovka .csv
    zadane_jmeno_souboru = sys.argv[2]
    if len(zadane_jmeno_souboru) < 5 or zadane_jmeno_souboru[-4:] != ".csv":
        print("Zkus zadat lépe název souboru")
        return False
    else:
        return True

def najdi_web_adresu(mesto, seznam):
# vytvoření web adresy pro vybraný uzemní celek
    pozice_seznam = 0
    web_adresa = list()
    while pozice_seznam < len(volebni_soup):
        if zadane_mesto in volebni_soup[pozice_seznam].text:
            # web adresa pro vytvoření hlavičky "csv" souboru
            web_adresa.append("https://volby.cz/pls/ps2017nss/" + str(volebni_soup[pozice_seznam-1].find("a"))[9:][:-12].replace("amp;",""))
            # web adresa pro scrapování územního celku
            web_adresa.append("https://volby.cz/pls/ps2017nss/" + str(volebni_soup[pozice_seznam+2].find("a"))[9:][:-7].replace("amp;",""))
            pozice_seznam += 1000
        pozice_seznam += 1
    return web_adresa

def vytvoreni_hlavicky(vstupni_argumenty, web_adresa):
# vytvoření hlavičky "csv" souboru
    hlavicka = requests.get(najdi_web_adresu(zadane_mesto, volebni_soup)[0])
    hlavicka_soup = BeautifulSoup(hlavicka.text, 'html.parser')
    hlavicka_zapis = ["kod","misto","registrovani_volici","odevzdane_obalky","platne_hlasy"]
    hlavicka_soup_1 = hlavicka_soup.find_all("td")
    for td in hlavicka_soup_1:
        if td['class'] == ['overflow_name']:
            hlavicka_zapis.append(td.text)
    return hlavicka_zapis

url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
volebni_okrsky = requests.get(url)
volebni_soup = BeautifulSoup(volebni_okrsky.text, 'html.parser').find_all("td")
zadane_mesto = sys.argv[1].replace("_"," ")
if kontrola_vstupnich_hodnot(sys.argv,seznam_uzemnich_celku(volebni_soup),zadane_mesto):
    volebni_okrsek = requests.get(najdi_web_adresu(zadane_mesto, volebni_soup)[1])
    zapis_csv = open(sys.argv[2], mode="w", newline="")
    zapis = csv.writer(zapis_csv, delimiter=",")
    zapis.writerow(vytvoreni_hlavicky(sys.argv, najdi_web_adresu(zadane_mesto, volebni_soup)[0]))
    volebni_okrsek_soup = BeautifulSoup(volebni_okrsek.text, 'html.parser').find_all("td")
    for poradi in range(len(volebni_okrsek_soup)):
        data_okrsek = list()
        if volebni_okrsek_soup[poradi]['class'] == ['cislo']:
            data_okrsek.append(volebni_okrsek_soup[poradi].text)
            data_okrsek.append(volebni_okrsek_soup[poradi+1].text)
            obec = requests.get("https://volby.cz/pls/ps2017nss/" + str(volebni_okrsek_soup[poradi].find("a"))[9:][:-12].replace("amp;",""))
            obec_soup = BeautifulSoup(obec.text, 'html.parser').find_all("td")
            for td in obec_soup: 
                if td['headers'] in (['sa2'],['sa5'],['sa6']):
                    data_okrsek.append(td.text.replace("\xa0",""))
            for poradi_1 in range(len(obec_soup)):
                if obec_soup[poradi_1]['class'] == ['overflow_name']:
                    data_okrsek.append(obec_soup[poradi_1+1].text.replace("\xa0",""))
            zapis.writerow(data_okrsek)
    zapis_csv.close()