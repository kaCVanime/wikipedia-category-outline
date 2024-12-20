import json
import re
import requests
from bs4 import BeautifulSoup, NavigableString
from pathlib import Path

proxies = {
    # "https": "http://127.0.0.1:7890"
}


def get_source():
    tgt = "https://en.wikipedia.org/wiki/Wikipedia:Contents/Categories"

    fp = Path('source_category.html')
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

    def _get_full_topic_name(self, el):
        title = el.get("title", '')
        s = 'Category:'
        return title[len(s):] if title.startswith(s) else el.get_text()

    def _get_children_names(self, lis):
        results = []
        for li in lis:
            if not (ul := li.ul):
                results.append(self._get_full_topic_name(li.a))
            else:
                t = li.find('a', recursive=False)
                name = self._get_full_topic_name(t)
                results.append(f'{name}({"·".join([a.get_text() for a in ul.find_all("a")])})')
        return results

    def _parse_h(self, h):
        uls = h.find_all('ul', recursive=False)
        assert len(uls) == 1, NotImplementedError
        lis = uls[0].find_all('li', recursive=False)
        b = lis[0].b
        header = lis[0].get_text() if b else None
        if lis[0].get_text().startswith('See also'):
            return []
        if header:
            return {
                "subject": header,
                "level": self._get_hs_level(h) + 2,
                "children": self._get_children_names(lis[1:]),
                "subcategory": []
            }
        return self._get_children_names(lis)

    def parse_content(self, content):
        hs = content.find_all('div', class_='hlist')
        tree = []
        stack = []
        for h in hs:
            cat = self._parse_h(h)
            if cat is None:
                continue
            if type(cat) is list:
                t = tree if not stack else stack[-1]["subcategory"]
                t.extend(cat)
                continue
            else:
                while stack and stack[-1]["level"] >= cat["level"]:
                    stack.pop()

                if stack:
                    stack[-1]["subcategory"].append(cat)
                else:
                    tree.append(cat)

                stack.append(cat)

        return tree


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
                    "children": self.parse_content(self.get_contents(e))
                } for e in self.get_entries()
            ], ft
        )

def main():
    parser = Parser(get_source())
    result = parser.run()
    with open('result_category.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(result, ensure_ascii=False))


main()
