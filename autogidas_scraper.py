import requests
from bs4 import BeautifulSoup
from time import sleep

def scrape_autogidas(kiek_pusl):
    visos_kainos = []
    for i in range(kiek_pusl):
        sleep(1)
        url = 'https://www.autogidas.lt/skelbimai/automobiliai/?f_1=Audi&f_50=kaina_asc&page=%s' % i
        r = requests.get(url)
        kainos = gauk_visas_kainas(r)
        visos_kainos += str(kainos)

    issaugoti_informacija_i_txt_faila(visos_kainos)
    
def issaugoti_informacija_i_txt_faila(visos_kainos):
    with open('kainos.txt', 'a') as f:
        f.write(visos_kainos + '\n')

def gauk_visas_kainas(r:requests.Response):
    """Gauna visas kainas is requests response"""
    soup = BeautifulSoup(r.text, 'lxml')

    kainos = []
    item_price_elements = soup.find_all('div', class_='item-price')
    for item_price_element in item_price_elements:
        kaina = apdorok_kainos_elementa(item_price_element)
        kainos.append(kaina)
    return kainos

def apdorok_kainos_elementa(item_price_element:BeautifulSoup):
    """"""
    text = item_price_element.get_text()
    kaina = text.strip()
    kaina_be_euro = kaina.split(' €')[0]
    kaina_be_tarpu = kaina_be_euro.replace(' ', '')
    return int(kaina_be_tarpu)
    

if __name__ == '__main__':
    while True:
        scrape_autogidas(5)
        sleep(60 * 60 * 24)
