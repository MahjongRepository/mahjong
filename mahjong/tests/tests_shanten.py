# -*- coding: utf-8 -*-
import unittest

from mahjong.shanten import Shanten
from mahjong.tests_mixin import TestMixin


class ShantenTestCase(unittest.TestCase, TestMixin):

    def test_shanten_number(self):
        shanten = Shanten()

        tiles = self._string_to_34_array(sou='111234567', pin='11', man='567')
        self.assertEqual(shanten.calculate_shanten(tiles), Shanten.AGARI_STATE)

        tiles = self._string_to_34_array(sou='111345677', pin='11', man='567')
        self.assertEqual(shanten.calculate_shanten(tiles), 0)

        tiles = self._string_to_34_array(sou='111345677', pin='15', man='567')
        self.assertEqual(shanten.calculate_shanten(tiles), 1)

        tiles = self._string_to_34_array(sou='11134567', pin='15', man='1578')
        self.assertEqual(shanten.calculate_shanten(tiles), 2)

        tiles = self._string_to_34_array(sou='113456', pin='1358', man='1358')
        self.assertEqual(shanten.calculate_shanten(tiles), 3)

        tiles = self._string_to_34_array(sou='1589', pin='13588', man='1358', honors='1')
        self.assertEqual(shanten.calculate_shanten(tiles), 4)

        tiles = self._string_to_34_array(sou='159', pin='13588', man='1358', honors='12')
        self.assertEqual(shanten.calculate_shanten(tiles), 5)

        tiles = self._string_to_34_array(sou='1589', pin='258', man='1358', honors='123')
        self.assertEqual(shanten.calculate_shanten(tiles), 6)

        tiles = self._string_to_34_array(sou='11123456788999')
        self.assertEqual(shanten.calculate_shanten(tiles), Shanten.AGARI_STATE)

        tiles = self._string_to_34_array(sou='11122245679999')
        self.assertEqual(shanten.calculate_shanten(tiles), 0)

    def test_shanten_number_and_chitoitsu(self):
        shanten = Shanten()

        tiles = self._string_to_34_array(sou='114477', pin='114477', man='77')
        self.assertEqual(shanten.calculate_shanten(tiles), Shanten.AGARI_STATE)

        tiles = self._string_to_34_array(sou='114477', pin='114477', man='76')
        self.assertEqual(shanten.calculate_shanten(tiles), 0)

        tiles = self._string_to_34_array(sou='114477', pin='114479', man='76')
        self.assertEqual(shanten.calculate_shanten(tiles), 1)

        tiles = self._string_to_34_array(sou='114477', pin='14479', man='76', honors='1')
        self.assertEqual(shanten.calculate_shanten(tiles), 2)

    def test_shanten_number_and_kokushi_musou(self):
        shanten = Shanten()

        tiles = self._string_to_34_array(sou='19', pin='19', man='19', honors='12345677')
        self.assertEqual(shanten.calculate_shanten(tiles), Shanten.AGARI_STATE)

        tiles = self._string_to_34_array(sou='129', pin='19', man='19', honors='1234567')
        self.assertEqual(shanten.calculate_shanten(tiles), 0)

        tiles = self._string_to_34_array(sou='129', pin='129', man='19', honors='123456')
        self.assertEqual(shanten.calculate_shanten(tiles), 1)

        tiles = self._string_to_34_array(sou='129', pin='129', man='129', honors='12345')
        self.assertEqual(shanten.calculate_shanten(tiles), 2)

    def test_shanten_number_and_open_sets(self):
        shanten = Shanten()

        tiles = self._string_to_34_array(sou='44467778', pin='222567')
        self.assertEqual(shanten.calculate_shanten(tiles), Shanten.AGARI_STATE)

        melds = [self._string_to_open_34_set(sou='777')]
        self.assertEqual(shanten.calculate_shanten(tiles, melds), 0)

        tiles = self._string_to_34_array(sou='23455567', pin='222', man='345')
        melds = [
            self._string_to_open_34_set(man='345'),
            self._string_to_open_34_set(sou='555'),
        ]
        self.assertEqual(shanten.calculate_shanten(tiles, melds), 0)
