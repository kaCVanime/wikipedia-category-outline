import json

import requests
from bs4 import BeautifulSoup, NavigableString
from pathlib import Path

proxies = {
    # "https": "http://127.0.0.1:7890"
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
        self.soup = BeautifulSoup(source, 'html.parser')

    def get_entries(self):
        return self.soup.find_all(class_='contentsPage__heading')

    def get_contents(self, e):
        return e.find_next_sibling(class_="contentsPage__section")

    def get_entry_name(self, entry):
        return entry.h2.get_text()

    def _is_content_header(self, tag):
        return tag.name == 'b' or tag.name == 'p' or tag.name == 'a' or (tag.name == 'i' and tag.a)

    def _get_headers(self, content):
        results = []
        children = content.contents
        uls = content.find_all('ul', recursive=False)
        h = None
        for idx, c in enumerate(children):
            if h and c.name == 'ul':
                results.append(h)
                h = None
                continue
            if self._is_content_header(c):
                if not uls:
                    results.append(c)
                    break
                h = c
                continue
            if type(c) is NavigableString and c != '\n':
                if not uls:
                    results.append(c)
                    break
                if idx == 0 and len(children) > 1 and children[idx + 1].name == 'ul':
                    h = c
                    continue
                if idx > 0 and children[idx - 1].name == 'ul' and (idx + 1 < len(children) - 1) and children[
                    idx + 1].name == 'ul':
                    h = c
                    continue
        return results

    def _get_header_text(self, h):
        s = h.get_text().strip()
        if ' – ' in s:
            s = s.split(' – ')[0]
        return s

    def _get_header_children(self, h):
        results = []
        n = h.next_sibling
        while n:
            if not n.name:
                n = n.next_sibling
                continue
            if n.name != 'ul':
                break

            results.append(n)
            n = n.next_sibling

        return results

    def parse_content(self, content, level):
        headers = self._get_headers(content)
        if not headers:
            return [self.parse_content(li, level) for ul in content.find_all('ul', recursive=False) for li in
                    ul.find_all('li', recursive=False)]
        results = []
        for h in headers:
            obj = {
                "subject": self._get_header_text(h),
                "level": level,
            }
            children = self._get_header_children(h)
            if children:
                obj["children"] = [self.parse_content(li, level + 1) for ul in children for li in
                                   ul.find_all('li', recursive=False)]
            results.append(obj)

        return results if len(results) > 1 else results[0]

    def format(self, tree):
        if not tree["children"]:
            tree.pop("children")
        else:
            for c in tree["children"]:
                self.format(c)
        return tree

    def _filter_by_level(self, tree, level):
        if tree["level"] > level:
            return None
        if "children" not in tree:
            return tree
        if tree["level"] == level:
            tree.pop("children")
            return tree
        tc = tree["children"]
        if type(tc) is list:
            tree["children"] = list(filter(lambda t: self._filter_by_level(t, level), tc))
        else:
            tree["children"] = self._filter_by_level(tc, level)
        if not tree["children"]:
            tree.pop("children")
        return tree

    def _filter(self, result, ft=None):
        if not ft:
            return result

        r = []
        for res in result:
            if (k := res["subject"]) not in ft:
                r.append(res)
            elif ft[k] == 0:
                continue
            else:
                r.append(self._filter_by_level(res, ft[k]))
        return list(filter(None, r))

    def run(self, ft=None):
        return self._filter(
            [
                {
                    "subject": self.get_entry_name(e),
                    "level": 1,
                    "children": self.parse_content(self.get_contents(e), 2)
                } for e in self.get_entries()
            ], ft
        )


# filter by level
my_filter = {
    "General reference": 0,
    "Culture and the arts": 5,
    "Geography and places": 1,
    "Health and fitness": 1,
    "History and events": 1,
    "Human activities": 3,
    "Mathematics and logic": 1,
    "Natural and physical sciences": 5,
    "People and self": 1,
    "Philosophy and thinking": 1,
    "Religion and belief systems": 1,
    "Society and social sciences": 3,
    "Technology and applied sciences": 4
}


def main():
    # mfilter = my_filter
    mfilter = None
    parser = Parser(get_source())
    result = parser.run(mfilter)
    with open('result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


main()
