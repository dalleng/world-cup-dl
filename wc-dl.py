# -*- coding: UTF-8 -*-

import csv
import requests
from bs4 import BeautifulSoup


def main():
    """
    Obtiene los primeros cuatro lugares en los mundiales de la
    FIFA y guarda los resultados en un archivo csv
    """
    competitions = []

    # inserta el nombre (sede y año) y los cuatros primeros en la lista
    # competitions
    for name, url in get_competition_links():
        competitions.append([name] + parse_competition(url))

    # escribe cada elemento de la lista competitions como una fila
    # en el archivo csv
    with open('world-cups.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Mundial', '1ro', '2do', '3ro', '4to'])

        for competition in competitions:
            writer.writerow(competition)


def get_competition_links():
    """
    Retorna el nombre y url de cada mundial
    """
    base_url = 'http://www.fifa.com'
    archive_url = '/fifa-tournaments/archive/worldcup/index.html'

    response = requests.get(base_url + archive_url)
    soup = BeautifulSoup(response.text)

    # itera sobre los links y retorna el nombre y la url del mundial
    for competition in soup.find_all(class_='comp-item'):
        competition_name = competition.find(class_='comp-name').text
        competition_url = base_url + competition.a['href']
        yield competition_name, competition_url


def parse_competition(url):
    """
    Retorna una lista con los cuatros primeros del mundial
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    return [t.text for t in soup.select('.c-team-rank .t-nText')]


if __name__ == '__main__':
    main()
