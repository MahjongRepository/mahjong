import pytest

from mahjong.constants import EAST, WEST
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.hand_calculating.scores import ScoresCalculator


@pytest.mark.parametrize(
    ("han", "fu", "expected_main"),
    [
        (1, 30, 1000),
        (1, 110, 3600),
        (2, 30, 2000),
        (3, 30, 3900),
        (4, 30, 7700),
        (4, 40, 8000),
        (5, 0, 8000),
        (6, 0, 12000),
        (8, 0, 16000),
        (11, 0, 24000),
        (13, 0, 32000),
        (26, 0, 64000),
        (39, 0, 96000),
        (52, 0, 128000),
        (65, 0, 160000),
        (78, 0, 192000),
    ],
)
def test_calculate_scores_and_ron(han: int, fu: int, expected_main: int) -> None:
    config = HandConfig(options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))
    result = ScoresCalculator.calculate_scores(han=han, fu=fu, config=config)
    assert result["main"] == expected_main


@pytest.mark.parametrize(
    ("han", "fu", "expected_main"),
    [
        (1, 30, 1500),
        (2, 30, 2900),
        (3, 30, 5800),
        (4, 30, 11600),
        (5, 0, 12000),
        (6, 0, 18000),
        (8, 0, 24000),
        (11, 0, 36000),
        (13, 0, 48000),
        (26, 0, 96000),
        (39, 0, 144000),
        (52, 0, 192000),
        (65, 0, 240000),
        (78, 0, 288000),
    ],
)
def test_calculate_scores_and_ron_by_dealer(han: int, fu: int, expected_main: int) -> None:
    config = HandConfig(player_wind=EAST, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))
    result = ScoresCalculator.calculate_scores(han=han, fu=fu, config=config)
    assert result["main"] == expected_main


@pytest.mark.parametrize(
    ("han", "fu", "expected_main", "expected_additional"),
    [
        (1, 30, 500, 300),
        (3, 30, 2000, 1000),
        (3, 60, 3900, 2000),
        (4, 30, 3900, 2000),
        (5, 0, 4000, 2000),
        (6, 0, 6000, 3000),
        (8, 0, 8000, 4000),
        (11, 0, 12000, 6000),
        (13, 0, 16000, 8000),
        (26, 0, 32000, 16000),
        (39, 0, 48000, 24000),
        (52, 0, 64000, 32000),
        (65, 0, 80000, 40000),
        (78, 0, 96000, 48000),
    ],
)
def test_calculate_scores_and_tsumo(han: int, fu: int, expected_main: int, expected_additional: int) -> None:
    config = HandConfig(is_tsumo=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))
    result = ScoresCalculator.calculate_scores(han=han, fu=fu, config=config)
    assert result["main"] == expected_main
    assert result["additional"] == expected_additional


@pytest.mark.parametrize(
    ("han", "fu", "expected_main", "expected_additional"),
    [
        (1, 30, 500, 500),
        (3, 30, 2000, 2000),
        (4, 30, 3900, 3900),
        (5, 0, 4000, 4000),
        (6, 0, 6000, 6000),
        (8, 0, 8000, 8000),
        (11, 0, 12000, 12000),
        (13, 0, 16000, 16000),
        (26, 0, 32000, 32000),
        (39, 0, 48000, 48000),
        (52, 0, 64000, 64000),
        (65, 0, 80000, 80000),
        (78, 0, 96000, 96000),
    ],
)
def test_calculate_scores_and_tsumo_by_dealer(han: int, fu: int, expected_main: int, expected_additional: int) -> None:
    config = HandConfig(player_wind=EAST, is_tsumo=True, options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))
    result = ScoresCalculator.calculate_scores(han=han, fu=fu, config=config)
    assert result["main"] == expected_main
    assert result["additional"] == expected_additional


def test_calculate_scores_with_bonus() -> None:
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


@pytest.mark.parametrize(
    ("player_wind", "han", "fu", "expected_main"),
    [
        (None, 4, 30, 8000),
        (None, 3, 60, 8000),
        (EAST, 4, 30, 12000),
        (EAST, 3, 60, 12000),
    ],
)
def test_kiriage_mangan(player_wind: int | None, han: int, fu: int, expected_main: int) -> None:
    config = HandConfig(player_wind=player_wind, options=OptionalRules(kiriage=True))
    result = ScoresCalculator.calculate_scores(han=han, fu=fu, config=config)
    assert result["main"] == expected_main


def test_calculate_scores_can_call_as_static_method() -> None:
    config = HandConfig(options=OptionalRules(kazoe_limit=HandConfig.KAZOE_NO_LIMIT))

    result = ScoresCalculator.calculate_scores(han=1, fu=30, config=config)
    assert result["main"] == 1000
