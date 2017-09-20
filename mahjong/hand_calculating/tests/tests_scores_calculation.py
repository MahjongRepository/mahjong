# -*- coding: utf-8 -*-
import unittest

from mahjong.hand_calculating.scores import ScoresCalculator


class ScoresCalculationTestCase(unittest.TestCase):

    def test_calculate_scores_and_ron(self):
        hand = ScoresCalculator()

        result = hand.calculate_scores(han=1, fu=30, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 1000)

        result = hand.calculate_scores(han=1, fu=110, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 3600)

        result = hand.calculate_scores(han=2, fu=30, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 2000)

        result = hand.calculate_scores(han=3, fu=30, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 3900)

        result = hand.calculate_scores(han=4, fu=30, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 7700)

        result = hand.calculate_scores(han=4, fu=40, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 8000)

        result = hand.calculate_scores(han=4, fu=40, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 12000)

        result = hand.calculate_scores(han=5, fu=0, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 8000)

        result = hand.calculate_scores(han=6, fu=0, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 12000)

        result = hand.calculate_scores(han=8, fu=0, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 16000)

        result = hand.calculate_scores(han=11, fu=0, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 24000)

        result = hand.calculate_scores(han=13, fu=0, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 32000)

        result = hand.calculate_scores(han=26, fu=0, is_tsumo=False, is_dealer=False)
        self.assertEqual(result['main'], 64000)

    def test_calculate_scores_and_ron_by_dealer(self):
        hand = ScoresCalculator()

        result = hand.calculate_scores(han=1, fu=30, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 1500)

        result = hand.calculate_scores(han=2, fu=30, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 2900)

        result = hand.calculate_scores(han=3, fu=30, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 5800)

        result = hand.calculate_scores(han=4, fu=30, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 11600)

        result = hand.calculate_scores(han=5, fu=0, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 12000)

        result = hand.calculate_scores(han=6, fu=0, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 18000)

        result = hand.calculate_scores(han=8, fu=0, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 24000)

        result = hand.calculate_scores(han=11, fu=0, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 36000)

        result = hand.calculate_scores(han=13, fu=0, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 48000)

        result = hand.calculate_scores(han=26, fu=0, is_tsumo=False, is_dealer=True)
        self.assertEqual(result['main'], 96000)

    def test_calculate_scores_and_tsumo(self):
        hand = ScoresCalculator()

        result = hand.calculate_scores(han=1, fu=30, is_tsumo=True, is_dealer=False)
        self.assertEqual(result['main'], 500)
        self.assertEqual(result['additional'], 300)

        result = hand.calculate_scores(han=3, fu=30, is_tsumo=True, is_dealer=False)
        self.assertEqual(result['main'], 2000)
        self.assertEqual(result['additional'], 1000)

        result = hand.calculate_scores(han=3, fu=60, is_tsumo=True, is_dealer=False)
        self.assertEqual(result['main'], 3900)
        self.assertEqual(result['additional'], 2000)

        result = hand.calculate_scores(han=4, fu=30, is_tsumo=True, is_dealer=False)
        self.assertEqual(result['main'], 3900)
        self.assertEqual(result['additional'], 2000)

        result = hand.calculate_scores(han=5, fu=0, is_tsumo=True, is_dealer=False)
        self.assertEqual(result['main'], 4000)
        self.assertEqual(result['additional'], 2000)

        result = hand.calculate_scores(han=6, fu=0, is_tsumo=True, is_dealer=False)
        self.assertEqual(result['main'], 6000)
        self.assertEqual(result['additional'], 3000)

        result = hand.calculate_scores(han=8, fu=0, is_tsumo=True, is_dealer=False)
        self.assertEqual(result['main'], 8000)
        self.assertEqual(result['additional'], 4000)

        result = hand.calculate_scores(han=11, fu=0, is_tsumo=True, is_dealer=False)
        self.assertEqual(result['main'], 12000)
        self.assertEqual(result['additional'], 6000)

        result = hand.calculate_scores(han=13, fu=0, is_tsumo=True, is_dealer=False)
        self.assertEqual(result['main'], 16000)
        self.assertEqual(result['additional'], 8000)

        result = hand.calculate_scores(han=26, fu=0, is_tsumo=True, is_dealer=False)
        self.assertEqual(result['main'], 32000)
        self.assertEqual(result['additional'], 16000)

    def test_calculate_scores_and_tsumo_by_dealer(self):
        hand = ScoresCalculator()

        result = hand.calculate_scores(han=1, fu=30, is_tsumo=True, is_dealer=True)
        self.assertEqual(result['main'], 500)
        self.assertEqual(result['additional'], 500)

        result = hand.calculate_scores(han=3, fu=30, is_tsumo=True, is_dealer=True)
        self.assertEqual(result['main'], 2000)
        self.assertEqual(result['additional'], 2000)

        result = hand.calculate_scores(han=4, fu=30, is_tsumo=True, is_dealer=True)
        self.assertEqual(result['main'], 3900)
        self.assertEqual(result['additional'], 3900)

        result = hand.calculate_scores(han=5, fu=0, is_tsumo=True, is_dealer=True)
        self.assertEqual(result['main'], 4000)
        self.assertEqual(result['additional'], 4000)

        result = hand.calculate_scores(han=6, fu=0, is_tsumo=True, is_dealer=True)
        self.assertEqual(result['main'], 6000)
        self.assertEqual(result['additional'], 6000)

        result = hand.calculate_scores(han=8, fu=0, is_tsumo=True, is_dealer=True)
        self.assertEqual(result['main'], 8000)
        self.assertEqual(result['additional'], 8000)

        result = hand.calculate_scores(han=11, fu=0, is_tsumo=True, is_dealer=True)
        self.assertEqual(result['main'], 12000)
        self.assertEqual(result['additional'], 12000)

        result = hand.calculate_scores(han=13, fu=0, is_tsumo=True, is_dealer=True)
        self.assertEqual(result['main'], 16000)
        self.assertEqual(result['additional'], 16000)

        result = hand.calculate_scores(han=26, fu=0, is_tsumo=True, is_dealer=True)
        self.assertEqual(result['main'], 32000)
        self.assertEqual(result['additional'], 32000)
