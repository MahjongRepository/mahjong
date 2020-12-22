# -*- coding: utf-8 -*-
import unittest

from mahjong.constants import EAST, SOUTH
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.yaku_config import YakuConfig
from mahjong.meld import Meld
from mahjong.tests_mixin import TestMixin


class HandResponseErrorTestCase(unittest.TestCase, TestMixin):
    def setUp(self):
        self.config = YakuConfig()

    def test_no_winning_tile(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="9")

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_riichi=True))
        self.assertEqual(result.error, "winning_tile_not_in_hand")

    def test_open_hand_riichi(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        melds = [self._make_meld(Meld.CHI, sou="123")]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds, config=self._make_hand_config(is_riichi=True))
        self.assertEqual(result.error, "open_hand_riichi_not_allowed")

    def test_open_hand_daburi(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        melds = [self._make_meld(Meld.CHI, sou="123")]
        result = hand.estimate_hand_value(
            tiles, win_tile, melds=melds, config=self._make_hand_config(is_riichi=True, is_daburu_riichi=True)
        )
        self.assertEqual(result.error, "open_hand_daburi_not_allowed")

    def test_ippatsu_without_riichi(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_ippatsu=True))
        self.assertEqual(result.error, "ippatsu_without_riichi_not_allowed")

    def test_hand_not_winning(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123344", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        result = hand.estimate_hand_value(tiles, win_tile)
        self.assertEqual(result.error, "hand_not_winning")

    def test_no_yaku(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        melds = [self._make_meld(Meld.CHI, sou="123")]
        result = hand.estimate_hand_value(tiles, win_tile, melds=melds)
        self.assertEqual(result.error, "no_yaku")

    def test_chankan_with_tsumo(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="1")

        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=True, is_chankan=True)
        )
        self.assertEqual(result.error, "chankan_with_tsumo_not_allowed")

    def test_rinshan_without_tsumo(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=False, is_rinshan=True)
        )
        self.assertEqual(result.error, "rinshan_without_tsumo_not_allowed")

    def test_haitei_without_tsumo(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=False, is_haitei=True)
        )
        self.assertEqual(result.error, "haitei_without_tsumo_not_allowed")

    def test_houtei_with_tsumo(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=True, is_houtei=True))
        self.assertEqual(result.error, "houtei_with_tsumo_not_allowed")

    def test_haitei_with_rinshan(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=True, is_rinshan=True, is_haitei=True)
        )
        self.assertEqual(result.error, "haitei_with_rinshan_not_allowed")

    def test_houtei_with_chankan(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="1")

        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=False, is_chankan=True, is_houtei=True)
        )
        self.assertEqual(result.error, "houtei_with_chankan_not_allowed")

    def test_tenhou_not_as_dealer(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        # no error when player wind is *not* specified
        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=True, is_tenhou=True))
        self.assertEqual(result.error, None)

        # raise error when player wind is specified and *not* EAST
        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=True, is_tenhou=True, player_wind=SOUTH)
        )
        self.assertEqual(result.error, "tenhou_not_as_dealer_not_allowed")

    def test_tenhou_without_tsumo(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=False, is_tenhou=True)
        )
        self.assertEqual(result.error, "tenhou_without_tsumo_not_allowed")

    def test_tenhou_with_meld(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="1234444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="1")

        melds = [self._make_meld(Meld.KAN, is_open=False, sou="4444")]
        result = hand.estimate_hand_value(
            tiles, win_tile, melds=melds, config=self._make_hand_config(is_tsumo=True, is_rinshan=True, is_tenhou=True)
        )
        self.assertEqual(result.error, "tenhou_with_meld_not_allowed")

    def test_chiihou_as_dealer(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        # no error when player wind is *not* specified
        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=True, is_chiihou=True)
        )
        self.assertEqual(result.error, None)

        # raise error when player wind is specified EAST
        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=True, is_chiihou=True, player_wind=EAST)
        )
        self.assertEqual(result.error, "chiihou_as_dealer_not_allowed")

    def test_chiihou_without_tsumo(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=False, is_chiihou=True)
        )
        self.assertEqual(result.error, "chiihou_without_tsumo_not_allowed")

    def test_chiihou_with_meld(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="1234444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="1")

        melds = [self._make_meld(Meld.KAN, is_open=False, sou="4444")]
        result = hand.estimate_hand_value(
            tiles, win_tile, melds=melds, config=self._make_hand_config(is_tsumo=True, is_rinshan=True, is_chiihou=True)
        )
        self.assertEqual(result.error, "chiihou_with_meld_not_allowed")

    def test_renhou_as_dealer(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        # no error when player wind is *not* specified
        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=False, is_renhou=True)
        )
        self.assertEqual(result.error, None)

        # raise error when player wind is specified EAST
        result = hand.estimate_hand_value(
            tiles, win_tile, config=self._make_hand_config(is_tsumo=False, is_renhou=True, player_wind=EAST)
        )
        self.assertEqual(result.error, "renhou_as_dealer_not_allowed")

    def test_renhou_with_tsumo(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="123444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="4")

        result = hand.estimate_hand_value(tiles, win_tile, config=self._make_hand_config(is_tsumo=True, is_renhou=True))
        self.assertEqual(result.error, "renhou_with_tsumo_not_allowed")

    def test_renhou_with_meld(self):
        hand = HandCalculator()

        tiles = self._string_to_136_array(sou="1234444", man="234456", pin="66")
        win_tile = self._string_to_136_tile(sou="1")

        melds = [self._make_meld(Meld.KAN, is_open=False, sou="4444")]
        result = hand.estimate_hand_value(
            tiles, win_tile, melds=melds, config=self._make_hand_config(is_tsumo=False, is_renhou=True)
        )
        self.assertEqual(result.error, "renhou_with_meld_not_allowed")
