import requests
import bs4
import sys
from bs4 import BeautifulSoup

def vytvoreni_souboru_vysledky_obce(vstupni_argumenty):
    # funkce, která vezme zadaný volební okrsek a vytvoří nový soubor s výsledky
    
    url = "https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    volebni_okrsky = requests.get(url)
    soup = BeautifulSoup(volebni_okrsky.text, 'html.parser')
    soup1 = soup.find_all("td")
    if kontrola_vstupnich_hodnot(sys.argv):
        print(soup1)

def kontrola_vstupnich_hodnot(vstupni_argumenty):
    if len(sys.argv) != 3:
        print("zadej 3 argumenty")

vytvoreni_souboru_vysledky_obce(sys.argv)