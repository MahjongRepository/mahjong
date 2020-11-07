# -*- coding: utf-8 -*-
import unittest

from mahjong.shanten import Shanten
from mahjong.tests_mixin import TestMixin


class ShantenTestCase(unittest.TestCase, TestMixin):
    def test_shanten_number(self):
        shanten = Shanten()

        tiles = self._string_to_34_array(sou="111234567", pin="11", man="567")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), Shanten.AGARI_STATE)

        tiles = self._string_to_34_array(sou="111345677", pin="11", man="567")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 0)

        tiles = self._string_to_34_array(sou="111345677", pin="15", man="567")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 1)

        tiles = self._string_to_34_array(sou="11134567", pin="15", man="1578")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 2)

        tiles = self._string_to_34_array(sou="113456", pin="1358", man="1358")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 3)

        tiles = self._string_to_34_array(sou="1589", pin="13588", man="1358", honors="1")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 4)

        tiles = self._string_to_34_array(sou="159", pin="13588", man="1358", honors="12")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 5)

        tiles = self._string_to_34_array(sou="1589", pin="258", man="1358", honors="123")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 6)

        tiles = self._string_to_34_array(sou="11123456788999")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), Shanten.AGARI_STATE)

        tiles = self._string_to_34_array(sou="11122245679999")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 0)

        tiles = self._string_to_34_array(sou="4566677", pin="1367", man="8", honors="12")
        self.assertEqual(shanten.calculate_shanten(tiles), 2)

        tiles = self._string_to_34_array(sou="14", pin="3356", man="3678", honors="2567")
        self.assertEqual(shanten.calculate_shanten(tiles), 4)

        tiles = self._string_to_34_array(sou="159", pin="17", man="359", honors="123567")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 7)

        tiles = self._string_to_34_array(man="1111222235555", honors="1")
        self.assertEqual(shanten.calculate_shanten(tiles), 0)

    def test_shanten_for_not_completed_hand(self):
        shanten = Shanten()

        tiles = self._string_to_34_array(sou="111345677", pin="1", man="567")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 1)

        tiles = self._string_to_34_array(sou="111345677", man="567")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 1)

        tiles = self._string_to_34_array(sou="111345677", man="56")
        self.assertEqual(shanten.calculate_shanten_for_regular_hand(tiles), 0)

    def test_shanten_number_and_chiitoitsu(self):
        shanten = Shanten()

        tiles = self._string_to_34_array(sou="114477", pin="114477", man="77")
        self.assertEqual(shanten.calculate_shanten_for_chiitoitsu_hand(tiles), Shanten.AGARI_STATE)

        tiles = self._string_to_34_array(sou="114477", pin="114477", man="76")
        self.assertEqual(shanten.calculate_shanten_for_chiitoitsu_hand(tiles), 0)

        tiles = self._string_to_34_array(sou="114477", pin="114479", man="76")
        self.assertEqual(shanten.calculate_shanten_for_chiitoitsu_hand(tiles), 1)

        tiles = self._string_to_34_array(sou="114477", pin="14479", man="76", honors="1")
        self.assertEqual(shanten.calculate_shanten_for_chiitoitsu_hand(tiles), 2)

        tiles = self._string_to_34_array(sou="114477", pin="13479", man="76", honors="1")
        self.assertEqual(shanten.calculate_shanten_for_chiitoitsu_hand(tiles), 3)

        tiles = self._string_to_34_array(sou="114467", pin="13479", man="76", honors="1")
        self.assertEqual(shanten.calculate_shanten_for_chiitoitsu_hand(tiles), 4)

        tiles = self._string_to_34_array(sou="114367", pin="13479", man="76", honors="1")
        self.assertEqual(shanten.calculate_shanten_for_chiitoitsu_hand(tiles), 5)

        tiles = self._string_to_34_array(sou="124367", pin="13479", man="76", honors="1")
        self.assertEqual(shanten.calculate_shanten_for_chiitoitsu_hand(tiles), 6)

    def test_shanten_number_and_kokushi(self):
        shanten = Shanten()

        tiles = self._string_to_34_array(sou="19", pin="19", man="19", honors="12345677")
        self.assertEqual(shanten.calculate_shanten_for_kokushi_hand(tiles), Shanten.AGARI_STATE)

        tiles = self._string_to_34_array(sou="129", pin="19", man="19", honors="1234567")
        self.assertEqual(shanten.calculate_shanten_for_kokushi_hand(tiles), 0)

        tiles = self._string_to_34_array(sou="129", pin="129", man="19", honors="123456")
        self.assertEqual(shanten.calculate_shanten_for_kokushi_hand(tiles), 1)

        tiles = self._string_to_34_array(sou="129", pin="129", man="129", honors="12345")
        self.assertEqual(shanten.calculate_shanten_for_kokushi_hand(tiles), 2)

        tiles = self._string_to_34_array(sou="1239", pin="129", man="129", honors="2345")
        self.assertEqual(shanten.calculate_shanten_for_kokushi_hand(tiles), 3)

        tiles = self._string_to_34_array(sou="1239", pin="1239", man="129", honors="345")
        self.assertEqual(shanten.calculate_shanten_for_kokushi_hand(tiles), 4)

        tiles = self._string_to_34_array(sou="1239", pin="1239", man="1239", honors="45")
        self.assertEqual(shanten.calculate_shanten_for_kokushi_hand(tiles), 5)

        tiles = self._string_to_34_array(sou="12349", pin="1239", man="1239", honors="5")
        self.assertEqual(shanten.calculate_shanten_for_kokushi_hand(tiles), 6)

        tiles = self._string_to_34_array(sou="12349", pin="12349", man="1239")
        self.assertEqual(shanten.calculate_shanten_for_kokushi_hand(tiles), 7)

    def test_shanten_number_and_open_sets(self):
        shanten = Shanten()

        tiles = self._string_to_34_array(sou="44467778", pin="222567")
        self.assertEqual(shanten.calculate_shanten(tiles), Shanten.AGARI_STATE)

        tiles = self._string_to_34_array(sou="44468", pin="222567")
        self.assertEqual(shanten.calculate_shanten(tiles), 0)

        tiles = self._string_to_34_array(sou="68", pin="222567")
        self.assertEqual(shanten.calculate_shanten(tiles), 0)

        tiles = self._string_to_34_array(sou="68", pin="567")
        self.assertEqual(shanten.calculate_shanten(tiles), 0)

        tiles = self._string_to_34_array(sou="68")
        self.assertEqual(shanten.calculate_shanten(tiles), 0)

        tiles = self._string_to_34_array(sou="88")
        self.assertEqual(shanten.calculate_shanten(tiles), Shanten.AGARI_STATE)
