# coding: utf8
from __future__ import unicode_literals, print_function
from django.test import TestCase
from hamcrest import *
from mock import patch, PropertyMock
import os
from feeds.models import Item
from kudago_parsers.kudago_parsers import Importer


def make_xml_path(path):
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(cwd, path)


class TestAfisha(TestCase):

    def test_regular(self):
        xml_path = make_xml_path('tests/afisha.xml')

        with patch('feeds.parsers.AfishaRssParser.url', new_callable=PropertyMock, return_value=xml_path):
            Importer().do_import(use_parsers=['afisha_gorod'])
            obj = Item.objects.get()
            assert_that(
                obj,
                has_properties(
                    title='Планы на выходные: «Скотобойня», парки, квесты '
                          'и еще 12 способов весело провести майские праздники',
                    link='http://gorod.afisha.ru/entertainment/skotoboynya-'
                         'parki-kvesty-i-eshche-12-sposobov-veselo-provesti-mayskie-prazdniki/',
                    value='На майские праздники принято уезжать или погружаться головой в череду пикников с шашлыками.'
                          'Для тех, у кого нет возможности, выбраться за город, «Афиша» нашла 15 интересных занятий на четыре выходных дня. '
                          'Открытие сезона в парках'
                )
            )

    def test_exclude(self):
        xml_path = make_xml_path('tests/afisha.xml')
        settings = {
            'afisha_gorod': {
                'parser': 'feeds.parsers.AfishaRssParser',
                'excludes': ['value']
            }
        }

        with patch('feeds.parsers.AfishaRssParser.url', new_callable=PropertyMock, return_value=xml_path):
            Importer().do_import(use_parsers=['afisha_gorod'], override_settings=settings)
            obj = Item.objects.get()
            assert_that(
                obj,
                has_properties(
                    title='Планы на выходные: «Скотобойня», парки, квесты '
                          'и еще 12 способов весело провести майские праздники',
                    link='http://gorod.afisha.ru/entertainment/skotoboynya-'
                         'parki-kvesty-i-eshche-12-sposobov-veselo-provesti-mayskie-prazdniki/',
                    value=''
                )
            )