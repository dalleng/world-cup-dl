import csv
import requests
from bs4 import BeautifulSoup


def main():
    competitions = []

    for name, url in get_competition_links():
        competitions.append([name] + parse_competition(url))

    with open('world-cups.csv', 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Mundial', '1ro', '2do', '3ro', '4to'])

        for competition in competitions:
            writer.writerow(competition)


def get_competition_links():
    base_url = 'http://www.fifa.com'
    archive_url = '/fifa-tournaments/archive/worldcup/index.html'

    response = requests.get(base_url + archive_url)
    soup = BeautifulSoup(response.text)

    for competition in soup.find_all(class_='comp-item'):
        competition_name = competition.find(class_='comp-name').text
        competition_url = base_url + competition.a['href']
        yield competition_name, competition_url


def parse_competition(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    return [t.text for t in soup.select('.c-team-rank .t-nText')]


if __name__ == '__main__':
    main()
