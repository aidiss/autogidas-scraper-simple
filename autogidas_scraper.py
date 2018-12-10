import requests
from bs4 import BeautifulSoup
from time import sleep
from argparse import ArgumentParser
import logging

DUMP_FILES = False

class Scraper:
    kiek_puslapiu = 3
    base_url = 'https://autogidas.lt/'
    logging_level = 'INFO'


    """This class is used to scrape data from autogidas.lt website"""
    def __init__(self, logger, writer, argument_parser):
        self.logger = logger
        self.writer = writer
        self.argument_parser = argument_parser

    def __gt__(self, other):
        return self.kiek_puslapiu > other.kiek_puslapiu


    def scrape(self, brand):
        self._scrape_autogidas(kiek_pusl=self.kiek_puslapiu, brand=brand)

    def _scrape_autogidas(self, kiek_pusl, brand):
        visos_kainos = []
        for i in range(1, kiek_pusl):
            sleep(1)
            url = self.base_url + 'skelbimai/automobiliai/?f_1=%s&f_50=kaina_asc&page=%s' % (brand, i)
            # url1 = 'https://autogidas.lt/skelbimai/automobiliai/?f_1=Audi&f_50=kaina_asc&page=1'
            logger.warning(url)
            r = requests.get(url)
            if 'Nerasta rezultat' in r.text:
                raise ValueError('Nerasta result')
            logger.warning(len(r.text))
            if DUMP_FILES:
                self.issaugoti_puslapio_kopija(i, r.text)
            kainos = self.gauk_visas_kainas(r)
            visos_kainos += str(kainos)

        self.issaugoti_informacija_i_txt_faila(visos_kainos)
        
    def issaugoti_puslapio_kopija(self, i, html_page):
        with open(str(i) + '.html', 'w', encoding='utf8') as f:
            f.write(html_page)

    def issaugoti_informacija_i_txt_faila(self, visos_kainos):
        with open('kainos.txt', 'a') as f:
            f.write(str(visos_kainos) + '\n')

    def gauk_visas_kainas(self, r: requests.Response):
        """Gauna visas kainas is requests response"""
        soup = BeautifulSoup(r.text, 'lxml')

        kainos = []
        item_price_elements = soup.find_all('div', class_='item-price')
        self.logger.info(len(item_price_elements))
        for item_price_element in item_price_elements:
            kaina = self.apdorok_kainos_elementa(item_price_element)
            self.logger.info(kaina)
            kainos.append(kaina)
        return kainos

    def apdorok_kainos_elementa(self, item_price_element: BeautifulSoup):
        """"""
        text = item_price_element.get_text()
        kaina = text.strip()
        kaina_be_euro = kaina.split(' €')[0]
        kaina_be_tarpu = kaina_be_euro.replace(' ', '')
        return int(kaina_be_tarpu)
    

class AudiScraper(Scraper):
    def scrape(self, brand='audi'):
        self._scrape_autogidas(kiek_pusl=1, brand=brand)


if __name__ == '__main__':
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.level = logging.DEBUG
    parser = ArgumentParser()
    parser.add_argument('brand')
    arguments = parser.parse_args()
    
    writer = ''
    scraper = Scraper(logger=logger, writer=writer, argument_parser=parser)

    while True:
        scraper.scrape(arguments.brand)
        sleep(60 * 60 * 24)
