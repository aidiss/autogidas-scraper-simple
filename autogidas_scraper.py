import requests
from bs4 import BeautifulSoup
from time import sleep

def gauk_visas_kainas(r):
    soup = BeautifulSoup(r.text, 'lxml')
    kainos = []
    for x in soup.find_all('div', class_='item-price'):
        text = x.get_text()
        kaina = text.strip()
        kaina_be_euro = kaina.split(' €')[0]
        kaina_be_tarpu = kaina_be_euro.replace(' ', '')
        kaina_int = int(kaina_be_tarpu)
        kainos.append(kaina_int)
    return kainos


def scrape_autogidas(kiek_pusl):
    visos_kainos = []
    for i in range(kiek_pusl):
        sleep(1)
        url = 'https://www.autogidas.lt/skelbimai/automobiliai/?f_1=Audi&f_50=kaina_asc&page=%s' % i
        p
        r = requests.get(url)
        kainos = gauk_visas_kainas(r)
        visos_kainos += kainos

    with open('kainos.txt', 'a') as f:
        f.write(str(visos_kainos) + '\n')

if __name__ == '__main__':
    while True:
        scrape_autogidas(5)
        sleep(60 * 60 * 24)











