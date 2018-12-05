import requests
from bs4 import BeautifulSoup
from time import sleep
from argparse import ArgumentParser
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

logger.warning('test warning')


def scrape_autogidas(kiek_pusl, brand):
    visos_kainos = []
    for i in range(1, kiek_pusl):
        sleep(1)
        url = 'https://autogidas.lt/skelbimai/automobiliai/?f_1=%s&f_50=kaina_asc&page=%s' % (brand, i)
        # url1 = 'https://autogidas.lt/skelbimai/automobiliai/?f_1=Audi&f_50=kaina_asc&page=1'
        logger.warning(url)
        r = requests.get(url)
        logger.warning(len(r.text))
        issaugoti_puslapio_kopija(i, r.text)
        kainos = gauk_visas_kainas(r)
        visos_kainos += str(kainos)

    issaugoti_informacija_i_txt_faila(visos_kainos)
    
def issaugoti_puslapio_kopija(i, html_page):
    with open(str(i) + '.html', 'w') as f:
        f.write(html_page)

def issaugoti_informacija_i_txt_faila(visos_kainos):
    with open('kainos.txt', 'a') as f:
        f.write(str(visos_kainos) + '\n')

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
    parser = ArgumentParser()
    parser.add_argument('brand')
    arguments = parser.parse_args()
    print(arguments)
    while True:
        scrape_autogidas(5,brand=arguments.brand)
        sleep(60 * 60 * 24)
