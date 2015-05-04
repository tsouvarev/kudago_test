from dateutil import parser
from feeds.models import Item
from kudago_parsers import BaseParser


class AfishaRssParser(BaseParser):

    url = 'http://gorod.afisha.ru/export/rss/'
    model = Item

    def parse(self):
        import feedparser
        return feedparser.parse(self.url)['entries']

    def get_title(self, item):
        return item['title']

    def get_link(self, item):
        return item['link']

    def get_time_published(self, item):
        return parser.parse(item['published'])

    def get_value(self, item):
        return item['description1'] + item['description2']