from bs4 import BeautifulSoup
import requests

def parse():
    url = 'https://omgtu.ru/general_information/the-structure/the-department-of-university.php'
    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    block = soup.find_all('div', class_='main__content')
    body = ''
    for data in block:
        if data.find('p'):
            body = data.text

    lines = body.split('\n')

    with open("departments.txt", "w", encoding="utf-8") as file:
        for element in lines:
            if element and element != 'Кафедры университета':
                file.write(element.strip() + "\n")

parse()