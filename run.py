import requests
from bs4 import BeautifulSoup
from pathlib import Path

proxies = {
    "https": "http://127.0.0.1:7890"
}


def get_source():
    tgt = "https://en.wikipedia.org/wiki/Wikipedia:Contents/Outlines"

    fp = Path('source.html')
    if fp.is_file():
        with open(fp, mode='r', encoding='utf-8') as f:
            return f.read()

    res = requests.get(tgt, proxies=proxies)
    with open(fp, mode='w', encoding='utf-8') as f:
        f.write(res.text)
        return res.text

class Parser:
    def __init__(self, source):
        self.soup = BeautifulSoup(source)

    def get_entries(self):
        return self.soup.find_all(class_='contentsPage__heading')

    def get_contents(self, e):
        return e.find_next_sibling(class_="contentsPage__section")

    def get_entry_name(self, entry):
        return entry.h2.get_text()
    def run(self):
        es = self.get_entries()
        root_names = [self.get_entry_name(e) for e in es]
        pass

def main():
    parser = Parser(get_source())
    parser.run()
    pass


main()
