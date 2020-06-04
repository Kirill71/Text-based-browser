import os
import sys
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore

init(autoreset=True)


class HtmlPrinter:
    SUPPORTED_TAGS = ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li')

    def __init__(self, text):
        self.__text = text

    def prettify(self):
        text = self.__text
        soup = BeautifulSoup(text, 'html.parser')
        all_text = ''
        HREF = 'a'
        for tag in soup.find_all(self.SUPPORTED_TAGS):
            if tag.name == HREF:
                all_text += Fore.BLUE

            all_text += tag.get_text().strip().replace('\n', ' ') + '\n' + Fore.RESET

        return all_text


class Browser:
    URL_PREFIX = 'https://'

    def __init__(self, dir_name):
        self.pages = []
        self.dir_name = dir_name
        try:
            os.mkdir(self.dir_name)
        except FileExistsError:
            pass

    def __validate(self, url):
        return url if url.startswith(self.URL_PREFIX) else self.URL_PREFIX + url

    def __get_url_name(self, url):
        short_url = url.replace(self.URL_PREFIX, '')
        return short_url[:short_url.find('.')]

    def back(self):
        if len(self.pages) > 2:
            print(self.pages[-2])

    def save(self, url, text):
        with open(f'{self.dir_name}//{self.__get_url_name(url)}.txt', 'w+') as f:
            f.write(text)

    def load(self, url):
        with open(f'{self.dir_name}//{self.__get_url_name(url)}.txt', 'r') as f:
            for line in f:
                print(line.split('\n')[0])

    def run(self):
        while True:
            url = input()

            if url == 'exit':
                break
            if url == 'back':
                self.back()

            url = self.__validate(url)

            if '.' in url:
                try:
                    response = requests.get(url)
                    printer = HtmlPrinter(response.text)
                    text = printer.prettify()
                    print(text)

                    self.pages.append(text)
                    self.save(url, text)

                except KeyError:
                    print('404 Error')
            else:
                try:
                    self.load(url)
                except FileNotFoundError:
                    print('Error: Incorrect URL')


def main():
    argv = sys.argv
    browser = Browser(argv[1])
    browser.run()


if __name__ == '__main__':
    main()
