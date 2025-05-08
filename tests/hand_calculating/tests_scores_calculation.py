from mahjong.constants import EAST, WEST
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.hand_calculating.scores import ScoresCalculator


def test_calculate_scores_and_ron():
    hand = ScoresCalculator()
    config = HandConfig(options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))

    result = hand.calculate_scores(han=1, fu=30, config=config)
    assert result["main"] == 1000

    result = hand.calculate_scores(han=1, fu=110, config=config)
    assert result["main"] == 3600

    result = hand.calculate_scores(han=2, fu=30, config=config)
    assert result["main"] == 2000

    result = hand.calculate_scores(han=3, fu=30, config=config)
    assert result["main"] == 3900

    result = hand.calculate_scores(han=4, fu=30, config=config)
    assert result["main"] == 7700

    result = hand.calculate_scores(han=4, fu=40, config=config)
    assert result["main"] == 8000

    result = hand.calculate_scores(han=5, fu=0, config=config)
    assert result["main"] == 8000

    result = hand.calculate_scores(han=6, fu=0, config=config)
    assert result["main"] == 12000

    result = hand.calculate_scores(han=8, fu=0, config=config)
    assert result["main"] == 16000

    result = hand.calculate_scores(han=11, fu=0, config=config)
    assert result["main"] == 24000

    result = hand.calculate_scores(han=13, fu=0, config=config)
    assert result["main"] == 32000

    result = hand.calculate_scores(han=26, fu=0, config=config)
    assert result["main"] == 64000

    result = hand.calculate_scores(han=39, fu=0, config=config)
    assert result["main"] == 96000

    result = hand.calculate_scores(han=52, fu=0, config=config)
    assert result["main"] == 128000

    result = hand.calculate_scores(han=65, fu=0, config=config)
    assert result["main"] == 160000

    result = hand.calculate_scores(han=78, fu=0, config=config)
    assert result["main"] == 192000


def test_calculate_scores_and_ron_by_dealer():
    hand = ScoresCalculator()
    config = HandConfig(player_wind=EAST, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))

    result = hand.calculate_scores(han=1, fu=30, config=config)
    assert result["main"] == 1500

    result = hand.calculate_scores(han=2, fu=30, config=config)
    assert result["main"] == 2900

    result = hand.calculate_scores(han=3, fu=30, config=config)
    assert result["main"] == 5800

    result = hand.calculate_scores(han=4, fu=30, config=config)
    assert result["main"] == 11600

    result = hand.calculate_scores(han=5, fu=0, config=config)
    assert result["main"] == 12000

    result = hand.calculate_scores(han=6, fu=0, config=config)
    assert result["main"] == 18000

    result = hand.calculate_scores(han=8, fu=0, config=config)
    assert result["main"] == 24000

    result = hand.calculate_scores(han=11, fu=0, config=config)
    assert result["main"] == 36000

    result = hand.calculate_scores(han=13, fu=0, config=config)
    assert result["main"] == 48000

    result = hand.calculate_scores(han=26, fu=0, config=config)
    assert result["main"] == 96000

    result = hand.calculate_scores(han=39, fu=0, config=config)
    assert result["main"] == 144000

    result = hand.calculate_scores(han=52, fu=0, config=config)
    assert result["main"] == 192000

    result = hand.calculate_scores(han=65, fu=0, config=config)
    assert result["main"] == 240000

    result = hand.calculate_scores(han=78, fu=0, config=config)
    assert result["main"] == 288000


def test_calculate_scores_and_tsumo():
    hand = ScoresCalculator()
    config = HandConfig(is_tsumo=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))

    result = hand.calculate_scores(han=1, fu=30, config=config)
    assert result["main"] == 500
    assert result["additional"] == 300

    result = hand.calculate_scores(han=3, fu=30, config=config)
    assert result["main"] == 2000
    assert result["additional"] == 1000

    result = hand.calculate_scores(han=3, fu=60, config=config)
    assert result["main"] == 3900
    assert result["additional"] == 2000

    result = hand.calculate_scores(han=4, fu=30, config=config)
    assert result["main"] == 3900
    assert result["additional"] == 2000

    result = hand.calculate_scores(han=5, fu=0, config=config)
    assert result["main"] == 4000
    assert result["additional"] == 2000

    result = hand.calculate_scores(han=6, fu=0, config=config)
    assert result["main"] == 6000
    assert result["additional"] == 3000

    result = hand.calculate_scores(han=8, fu=0, config=config)
    assert result["main"] == 8000
    assert result["additional"] == 4000

    result = hand.calculate_scores(han=11, fu=0, config=config)
    assert result["main"] == 12000
    assert result["additional"] == 6000

    result = hand.calculate_scores(han=13, fu=0, config=config)
    assert result["main"] == 16000
    assert result["additional"] == 8000

    result = hand.calculate_scores(han=26, fu=0, config=config)
    assert result["main"] == 32000
    assert result["additional"] == 16000

    result = hand.calculate_scores(han=39, fu=0, config=config)
    assert result["main"] == 48000
    assert result["additional"] == 24000

    result = hand.calculate_scores(han=52, fu=0, config=config)
    assert result["main"] == 64000
    assert result["additional"] == 32000

    result = hand.calculate_scores(han=65, fu=0, config=config)
    assert result["main"] == 80000
    assert result["additional"] == 40000

    result = hand.calculate_scores(han=78, fu=0, config=config)
    assert result["main"] == 96000
    assert result["additional"] == 48000


def test_calculate_scores_and_tsumo_by_dealer():
    hand = ScoresCalculator()
    config = HandConfig(player_wind=EAST, is_tsumo=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))

    result = hand.calculate_scores(han=1, fu=30, config=config)
    assert result["main"] == 500
    assert result["additional"] == 500

    result = hand.calculate_scores(han=3, fu=30, config=config)
    assert result["main"] == 2000
    assert result["additional"] == 2000

    result = hand.calculate_scores(han=4, fu=30, config=config)
    assert result["main"] == 3900
    assert result["additional"] == 3900

    result = hand.calculate_scores(han=5, fu=0, config=config)
    assert result["main"] == 4000
    assert result["additional"] == 4000

    result = hand.calculate_scores(han=6, fu=0, config=config)
    assert result["main"] == 6000
    assert result["additional"] == 6000

    result = hand.calculate_scores(han=8, fu=0, config=config)
    assert result["main"] == 8000
    assert result["additional"] == 8000

    result = hand.calculate_scores(han=11, fu=0, config=config)
    assert result["main"] == 12000
    assert result["additional"] == 12000

    result = hand.calculate_scores(han=13, fu=0, config=config)
    assert result["main"] == 16000
    assert result["additional"] == 16000

    result = hand.calculate_scores(han=26, fu=0, config=config)
    assert result["main"] == 32000
    assert result["additional"] == 32000

    result = hand.calculate_scores(han=39, fu=0, config=config)
    assert result["main"] == 48000
    assert result["additional"] == 48000

    result = hand.calculate_scores(han=52, fu=0, config=config)
    assert result["main"] == 64000
    assert result["additional"] == 64000

    result = hand.calculate_scores(han=65, fu=0, config=config)
    assert result["main"] == 80000
    assert result["additional"] == 80000

    result = hand.calculate_scores(han=78, fu=0, config=config)
    assert result["main"] == 96000
    assert result["additional"] == 96000


def test_calculate_scores_with_bonus():
    hand = ScoresCalculator()

    config = HandConfig(player_wind=EAST, is_tsumo=True, tsumi_number=2, kyoutaku_number=3)
    result = hand.calculate_scores(han=3, fu=30, config=config)
    assert result["main"] == 2000
    assert result["additional"] == 2000
    assert result["main_bonus"] == 200
    assert result["additional_bonus"] == 200
    assert result["kyoutaku_bonus"] == 3000
    assert result["total"] == 9600

    config = HandConfig(player_wind=WEST, is_tsumo=True, tsumi_number=4, kyoutaku_number=1)
    result = hand.calculate_scores(han=4, fu=30, config=config)
    assert result["main"] == 3900
    assert result["additional"] == 2000
    assert result["main_bonus"] == 400
    assert result["additional_bonus"] == 400
    assert result["kyoutaku_bonus"] == 1000
    assert result["total"] == 10100

    config = HandConfig(player_wind=WEST, tsumi_number=5)
    result = hand.calculate_scores(han=6, fu=30, config=config)
    assert result["main"] == 12000
    assert result["additional"] == 0
    assert result["main_bonus"] == 1500
    assert result["additional_bonus"] == 0
    assert result["kyoutaku_bonus"] == 0
    assert result["total"] == 13500

    config = HandConfig(player_wind=EAST, tsumi_number=5)
    result = hand.calculate_scores(han=5, fu=30, config=config)
    assert result["main"] == 12000
    assert result["additional"] == 0
    assert result["main_bonus"] == 1500
    assert result["additional_bonus"] == 0
    assert result["kyoutaku_bonus"] == 0
    assert result["total"] == 13500


def test_kiriage_mangan():
    hand = ScoresCalculator()

    config = HandConfig(options=OptionalRules(kiriage=True))

    result = hand.calculate_scores(han=4, fu=30, config=config)
    assert result["main"] == 8000

    result = hand.calculate_scores(han=3, fu=60, config=config)
    assert result["main"] == 8000

    config = HandConfig(player_wind=EAST, options=OptionalRules(kiriage=True))

    result = hand.calculate_scores(han=4, fu=30, config=config)
    assert result["main"] == 12000

    result = hand.calculate_scores(han=3, fu=60, config=config)
    assert result["main"] == 12000
