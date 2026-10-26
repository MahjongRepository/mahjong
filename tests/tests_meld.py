import pytest

from mahjong.meld import Meld
from mahjong.tile import TilesConverter
from tests.utils_for_tests import _make_meld


def test_meld_str() -> None:
    tiles = TilesConverter.string_to_136_array(man="123")
    meld = Meld(meld_type=Meld.CHI, tiles=tiles)
    assert str(meld) == f"Type: chi, Tiles: 123m {tuple(tiles)}"


def test_meld_repr() -> None:
    tiles = TilesConverter.string_to_136_array(man="111")
    meld = Meld(meld_type=Meld.PON, tiles=tiles)
    assert repr(meld) == str(meld)


def test_tiles_34_updates_on_tiles_reassignment() -> None:
    tiles = TilesConverter.string_to_136_array(man="111")
    meld = Meld(meld_type=Meld.PON, tiles=tiles)
    assert meld.tiles_34 == [0, 0, 0]

    new_tiles = TilesConverter.string_to_136_array(man="1111")
    meld.tiles = tuple(new_tiles)
    assert meld.tiles_34 == [0, 0, 0, 0]


@pytest.mark.parametrize(
    "meld",
    [
        pytest.param(_make_meld(Meld.CHI, man="123"), id="chi"),
        pytest.param(_make_meld(Meld.CHI, sou="789"), id="chi_789"),
        pytest.param(_make_meld(Meld.PON, honors="555"), id="pon"),
        pytest.param(_make_meld(Meld.KAN, man="1111"), id="open_kan"),
        pytest.param(_make_meld(Meld.KAN, is_open=False, man="1111"), id="closed_kan"),
        pytest.param(_make_meld(Meld.SHOUMINKAN, man="1111"), id="shouminkan"),
        pytest.param(_make_meld(Meld.NUKI, honors="4"), id="nuki"),
        pytest.param(_make_meld(Meld.NUKI, is_open=False, honors="4"), id="closed_nuki"),
        pytest.param(_make_meld(Meld.NUKI, honors="44"), id="nuki_two_tiles"),
        pytest.param(_make_meld(Meld.NUKI, honors="4444"), id="nuki_four_tiles"),
    ],
)
def test_is_valid(meld: Meld) -> None:
    assert meld.is_valid()


@pytest.mark.parametrize(
    ("meld_type", "meld_tiles"),
    [
        pytest.param("bad", TilesConverter.string_to_136_array(man="111"), id="unknown_type"),
        pytest.param(Meld.NUKI, TilesConverter.string_to_136_array(honors="1"), id="nuki_not_north"),
        pytest.param(Meld.NUKI, TilesConverter.string_to_136_array(honors="14"), id="nuki_mixed_tiles"),
        pytest.param(Meld.NUKI, [*TilesConverter.string_to_136_array(honors="4444"), 120], id="nuki_five_tiles"),
        pytest.param(Meld.NUKI, [], id="nuki_empty"),
        pytest.param(Meld.CHI, TilesConverter.string_to_136_array(man="89", pin="1"), id="chi_across_suits"),
        pytest.param(Meld.CHI, TilesConverter.string_to_136_array(sou="9", honors="12"), id="chi_into_honors"),
        pytest.param(Meld.CHI, TilesConverter.string_to_136_array(honors="123"), id="chi_of_honors"),
        pytest.param(Meld.CHI, TilesConverter.string_to_136_array(man="112"), id="chi_not_sequence"),
        pytest.param(Meld.CHI, TilesConverter.string_to_136_array(man="1234"), id="chi_four_tiles"),
        pytest.param(Meld.CHI, [], id="chi_empty"),
        pytest.param(Meld.PON, TilesConverter.string_to_136_array(man="1"), id="pon_one_tile"),
        pytest.param(Meld.PON, TilesConverter.string_to_136_array(man="123"), id="pon_of_sequence"),
        pytest.param(Meld.PON, TilesConverter.string_to_136_array(man="1111"), id="pon_four_tiles"),
        pytest.param(Meld.PON, [], id="pon_empty"),
        pytest.param(Meld.KAN, TilesConverter.string_to_136_array(man="111"), id="kan_three_tiles"),
        pytest.param(Meld.KAN, TilesConverter.string_to_136_array(man="1112"), id="kan_mixed_tiles"),
        pytest.param(Meld.SHOUMINKAN, TilesConverter.string_to_136_array(man="1112"), id="shouminkan_mixed_tiles"),
    ],
)
def test_is_valid_rejects_invalid_tiles(meld_type: str, meld_tiles: list[int]) -> None:
    assert not Meld(meld_type=meld_type, tiles=meld_tiles).is_valid()


@pytest.mark.parametrize(
    "meld",
    [
        pytest.param(_make_meld(Meld.CHI, is_open=False, man="123"), id="chi"),
        pytest.param(_make_meld(Meld.PON, is_open=False, man="111"), id="pon"),
        pytest.param(_make_meld(Meld.SHOUMINKAN, is_open=False, man="1111"), id="shouminkan"),
    ],
)
def test_is_valid_rejects_closed_meld_other_than_kan(meld: Meld) -> None:
    assert not meld.is_valid()
