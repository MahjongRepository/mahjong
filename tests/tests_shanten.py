from tile import TilesConverter

from mahjong.shanten import Shanten


def test_shanten_number():
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou="111234567", pin="11", man="567")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == Shanten.AGARI_STATE

    tiles = TilesConverter.string_to_34_array(sou="111345677", pin="11", man="567")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 0

    tiles = TilesConverter.string_to_34_array(sou="111345677", pin="15", man="567")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 1

    tiles = TilesConverter.string_to_34_array(sou="11134567", pin="15", man="1578")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 2

    tiles = TilesConverter.string_to_34_array(sou="113456", pin="1358", man="1358")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 3

    tiles = TilesConverter.string_to_34_array(sou="1589", pin="13588", man="1358", honors="1")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 4

    tiles = TilesConverter.string_to_34_array(sou="159", pin="13588", man="1358", honors="12")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 5

    tiles = TilesConverter.string_to_34_array(sou="1589", pin="258", man="1358", honors="123")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 6

    tiles = TilesConverter.string_to_34_array(sou="11123456788999")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == Shanten.AGARI_STATE

    tiles = TilesConverter.string_to_34_array(sou="11122245679999")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 0

    tiles = TilesConverter.string_to_34_array(sou="4566677", pin="1367", man="8", honors="12")
    assert shanten.calculate_shanten(tiles) == 2

    tiles = TilesConverter.string_to_34_array(sou="14", pin="3356", man="3678", honors="2567")
    assert shanten.calculate_shanten(tiles) == 4

    tiles = TilesConverter.string_to_34_array(sou="159", pin="17", man="359", honors="123567")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 7

    tiles = TilesConverter.string_to_34_array(man="1111222235555", honors="1")
    assert shanten.calculate_shanten(tiles) == 0


def test_shanten_for_not_completed_hand():
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou="111345677", pin="1", man="567")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 1

    tiles = TilesConverter.string_to_34_array(sou="111345677", man="567")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 1

    tiles = TilesConverter.string_to_34_array(sou="111345677", man="56")
    assert shanten.calculate_shanten_for_regular_hand(tiles) == 0


def test_shanten_number_and_chiitoitsu():
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou="114477", pin="114477", man="77")
    assert shanten.calculate_shanten_for_chiitoitsu_hand(tiles) == Shanten.AGARI_STATE

    tiles = TilesConverter.string_to_34_array(sou="114477", pin="114477", man="76")
    assert shanten.calculate_shanten_for_chiitoitsu_hand(tiles) == 0

    tiles = TilesConverter.string_to_34_array(sou="114477", pin="114479", man="76")
    assert shanten.calculate_shanten_for_chiitoitsu_hand(tiles) == 1

    tiles = TilesConverter.string_to_34_array(sou="114477", pin="14479", man="76", honors="1")
    assert shanten.calculate_shanten_for_chiitoitsu_hand(tiles) == 2

    tiles = TilesConverter.string_to_34_array(sou="114477", pin="13479", man="76", honors="1")
    assert shanten.calculate_shanten_for_chiitoitsu_hand(tiles) == 3

    tiles = TilesConverter.string_to_34_array(sou="114467", pin="13479", man="76", honors="1")
    assert shanten.calculate_shanten_for_chiitoitsu_hand(tiles) == 4

    tiles = TilesConverter.string_to_34_array(sou="114367", pin="13479", man="76", honors="1")
    assert shanten.calculate_shanten_for_chiitoitsu_hand(tiles) == 5

    tiles = TilesConverter.string_to_34_array(sou="124367", pin="13479", man="76", honors="1")
    assert shanten.calculate_shanten_for_chiitoitsu_hand(tiles) == 6


def test_shanten_number_and_kokushi():
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou="19", pin="19", man="19", honors="12345677")
    assert shanten.calculate_shanten_for_kokushi_hand(tiles) == Shanten.AGARI_STATE

    tiles = TilesConverter.string_to_34_array(sou="129", pin="19", man="19", honors="1234567")
    assert shanten.calculate_shanten_for_kokushi_hand(tiles) == 0

    tiles = TilesConverter.string_to_34_array(sou="129", pin="129", man="19", honors="123456")
    assert shanten.calculate_shanten_for_kokushi_hand(tiles) == 1

    tiles = TilesConverter.string_to_34_array(sou="129", pin="129", man="129", honors="12345")
    assert shanten.calculate_shanten_for_kokushi_hand(tiles) == 2

    tiles = TilesConverter.string_to_34_array(sou="1239", pin="129", man="129", honors="2345")
    assert shanten.calculate_shanten_for_kokushi_hand(tiles) == 3

    tiles = TilesConverter.string_to_34_array(sou="1239", pin="1239", man="129", honors="345")
    assert shanten.calculate_shanten_for_kokushi_hand(tiles) == 4

    tiles = TilesConverter.string_to_34_array(sou="1239", pin="1239", man="1239", honors="45")
    assert shanten.calculate_shanten_for_kokushi_hand(tiles) == 5

    tiles = TilesConverter.string_to_34_array(sou="12349", pin="1239", man="1239", honors="5")
    assert shanten.calculate_shanten_for_kokushi_hand(tiles) == 6

    tiles = TilesConverter.string_to_34_array(sou="12349", pin="12349", man="1239")
    assert shanten.calculate_shanten_for_kokushi_hand(tiles) == 7


def test_shanten_number_and_open_sets():
    shanten = Shanten()

    tiles = TilesConverter.string_to_34_array(sou="44467778", pin="222567")
    assert shanten.calculate_shanten(tiles) == Shanten.AGARI_STATE

    tiles = TilesConverter.string_to_34_array(sou="44468", pin="222567")
    assert shanten.calculate_shanten(tiles) == 0

    tiles = TilesConverter.string_to_34_array(sou="68", pin="222567")
    assert shanten.calculate_shanten(tiles) == 0

    tiles = TilesConverter.string_to_34_array(sou="68", pin="567")
    assert shanten.calculate_shanten(tiles) == 0

    tiles = TilesConverter.string_to_34_array(sou="68")
    assert shanten.calculate_shanten(tiles) == 0

    tiles = TilesConverter.string_to_34_array(sou="88")
    assert shanten.calculate_shanten(tiles) == Shanten.AGARI_STATE
