# -*- coding: utf-8 -*-
import unittest

from mahjong.agari import Agari
from mahjong.tests_mixin import TestMixin


class AgariTestCase(unittest.TestCase, TestMixin):

    def test_is_agari(self):
        agari = Agari()

        tiles = self._string_to_34_array(sou='123456789', pin='123', man='33')
        self.assertTrue(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='123456789', pin='11123')
        self.assertTrue(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='123456789', honors='11777')
        self.assertTrue(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='12345556778899')
        self.assertTrue(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='11123456788999')
        self.assertTrue(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='233334', pin='789', man='345', honors='55')
        self.assertTrue(agari.is_agari(tiles))

    def test_is_not_agari(self):
        agari = Agari()

        tiles = self._string_to_34_array(sou='123456789', pin='12345')
        self.assertFalse(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='111222444', pin='11145')
        self.assertFalse(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='11122233356888')
        self.assertFalse(agari.is_agari(tiles))

    def test_is_chitoitsu_agari(self):
        agari = Agari()

        tiles = self._string_to_34_array(sou='1133557799', pin='1199')
        self.assertTrue(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='2244', pin='1199', man='11', honors='2277')
        self.assertTrue(agari.is_agari(tiles))

        tiles = self._string_to_34_array(man='11223344556677')
        self.assertTrue(agari.is_agari(tiles))

    def test_is_kokushi_musou_agari(self):
        agari = Agari()

        tiles = self._string_to_34_array(sou='19', pin='19', man='199', honors='1234567')
        self.assertTrue(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='19', pin='19', man='19', honors='11234567')
        self.assertTrue(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='19', pin='19', man='19', honors='12345677')
        self.assertTrue(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='129', pin='19', man='19', honors='1234567')
        self.assertFalse(agari.is_agari(tiles))

        tiles = self._string_to_34_array(sou='19', pin='19', man='19', honors='11134567')
        self.assertFalse(agari.is_agari(tiles))

    def test_is_agari_and_open_hand(self):
        agari = Agari()

        tiles = self._string_to_34_array(sou='23455567', pin='222', man='345')
        melds = [
            self._string_to_open_34_set(man='345'),
            self._string_to_open_34_set(sou='555'),
        ]
        self.assertFalse(agari.is_agari(tiles, melds))
