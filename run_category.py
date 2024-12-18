import json
import re
import requests
from bs4 import BeautifulSoup, NavigableString
from pathlib import Path

proxies = {
    "https": "http://127.0.0.1:7890"
}


def get_source():
    tgt = "https://en.wikipedia.org/wiki/Wikipedia:Contents/Categories"

    fp = Path('category_source.html')
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

    def _get_hs_level(self, h):
        style = h["style"]
        r = re.search('margin-left:(.*?)em', style)
        if r:
            return int(float(r.group(1)))
        return 0

    def _get_children(self, lis):
        results = []
        for li in lis:

            if not (ul := li.ul):
                return li.get_text()
            else:
                t = li.find('a', recursive=False)
                name = t.get_text() if t else ''

    def _parse_h(self, h, level):
        uls = h.find_all('ul', recursive=False)
        assert len(uls) == 1, NotImplementedError
        lis = uls[0].find_all('li', recursive=False)
        b = lis[0].b
        header = b.get_text() if b else None
        if header:
            if header.startswith('See also'):
                return None
            return {
                "subject": header,
                "level": level,
                "children": [s for l in lis[1:] if not (s := l.get_text()).startswith('See also')],
                "subcategory": []
            }
        return [l.get_text() for l in lis]

    def _parse(self, hs, i, level):
        results = []
        while i < len(hs):
            h = hs[i]
            cat = self._parse_h(h, level)
            if cat is None:
                i = i + 1
                continue
            elif type(cat) is list:
                results.extend(cat)
                i = i + 1
                continue
            else:
                level = self._get_hs_level(h)
                p = i
                while (p := p+1) < len(hs):
                    next_h_level = self._get_hs_level(hs[p])
                    if next_h_level <= level:
                        break
                    if next_h_level == level + 1:
                        cat["subcategory"].append(self._parse(hs, p, level+1))
                    if next_h_level > level + 1:
                        continue

                results.append(cat)
                i = p

        return results


    def parse_content(self, content, level):
        hs = content.find_all('div', class_='hlist')
        return self._parse(hs, 0, level)


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
    with open('category_result.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


main()