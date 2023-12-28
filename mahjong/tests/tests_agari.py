from tile import TilesConverter
from utils_for_tests import _string_to_open_34_set

from mahjong.agari import Agari


def test_is_agari():
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou="123456789", pin="123", man="33")
    assert agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="123456789", pin="11123")
    assert agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="123456789", honors="11777")
    assert agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="12345556778899")
    assert agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="11123456788999")
    assert agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="233334", pin="789", man="345", honors="55")
    assert agari.is_agari(tiles)


def test_is_not_agari():
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou="123456789", pin="12345")
    assert not agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="111222444", pin="11145")
    assert not agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="11122233356888")
    assert not agari.is_agari(tiles)


def test_is_chitoitsu_agari():
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou="1133557799", pin="1199")
    assert agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="2244", pin="1199", man="11", honors="2277")
    assert agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(man="11223344556677")
    assert agari.is_agari(tiles)


def test_is_kokushi_musou_agari():
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou="19", pin="19", man="199", honors="1234567")
    assert agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="19", pin="19", man="19", honors="11234567")
    assert agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="19", pin="19", man="19", honors="12345677")
    assert agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="129", pin="19", man="19", honors="1234567")
    assert not agari.is_agari(tiles)

    tiles = TilesConverter.string_to_34_array(sou="19", pin="19", man="19", honors="11134567")
    assert not agari.is_agari(tiles)


def test_is_agari_and_open_hand():
    agari = Agari()

    tiles = TilesConverter.string_to_34_array(sou="23455567", pin="222", man="345")
    melds = [
        _string_to_open_34_set(man="345"),
        _string_to_open_34_set(sou="555"),
    ]
    assert not agari.is_agari(tiles, melds)
