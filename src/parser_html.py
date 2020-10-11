import re
import os

from html.parser import HTMLParser

class ParsingError(Exception):
    pass

class Parser(HTMLParser):

    def error(self, message):
        raise ParsingError(message)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs = dict(attrs)
            link = attrs['href']

            if not link.startswith('http'):
                hash_index = link.rfind('#')
                if hash_index > -1:
                    link = link[:hash_index]

                if link.endswith('html') or link.endswith('htm'):
                    relative_path = os.path.join(self.path_root, link)
                    link_path = os.path.abspath(relative_path)
                    self.links.append(link_path)

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        stripped_text = re.sub('[\W]', ' ', data).split()
        if stripped_text:
            self.words.extend(stripped_text)

    def parse(self, path):
        self.links = []
        self.words = []

        try:
            with open(path, 'r', encoding='utf8') as document:
                self.path_root = os.path.abspath(os.path.dirname(path))
                content = document.read()
                self.feed(content)

                self.links = list(set(self.links))

        except IOError as e:
            print(e)
        finally:
            return self.links, self.words
