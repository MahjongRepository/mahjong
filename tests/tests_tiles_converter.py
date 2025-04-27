from mahjong.constants import FIVE_RED_PIN
from mahjong.tile import TilesConverter


def test_convert_to_one_line_string():
    tiles = [0, 1, 34, 35, 36, 37, 70, 71, 72, 73, 106, 107, 108, 109, 133, 134]
    result = TilesConverter.to_one_line_string(tiles)
    assert "1199m1199p1199s1177z" == result


def test_convert_to_one_line_string_with_aka_dora():
    tiles = [1, 16, 13, 46, 5, 13, 24, 34, 134, 124]
    result = TilesConverter.to_one_line_string(tiles, print_aka_dora=False)
    assert "1244579m3p57z" == result
    result = TilesConverter.to_one_line_string(tiles, print_aka_dora=True)
    assert "1244079m3p57z" == result


def test_convert_to_34_array():
    tiles = [0, 34, 35, 36, 37, 70, 71, 72, 73, 106, 107, 108, 109, 134]
    result = TilesConverter.to_34_array(tiles)
    assert result[0] == 1
    assert result[8] == 2
    assert result[9] == 2
    assert result[17] == 2
    assert result[18] == 2
    assert result[26] == 2
    assert result[27] == 2
    assert result[33] == 1
    assert sum(result) == 14


def test_convert_to_136_array():
    tiles = [0, 32, 33, 36, 37, 68, 69, 72, 73, 104, 105, 108, 109, 132]
    result = TilesConverter.to_34_array(tiles)
    result = TilesConverter.to_136_array(result)
    assert result == tiles


def test_convert_string_to_136_array():
    tiles = TilesConverter.string_to_136_array(sou="19", pin="19", man="19", honors="1234567")

    assert [0, 32, 36, 68, 72, 104, 108, 112, 116, 120, 124, 128, 132] == tiles


def test_find_34_tile_in_136_array():
    result = TilesConverter.find_34_tile_in_136_array(0, [3, 4, 5, 6])
    assert result == 3

    result = TilesConverter.find_34_tile_in_136_array(33, [3, 4, 134, 135])
    assert result == 134

    result = TilesConverter.find_34_tile_in_136_array(20, [3, 4, 134, 135])
    assert result is None


def test_convert_string_with_aka_dora_to_136_array():
    tiles = TilesConverter.string_to_136_array(man="22444", pin="333r67", sou="444", has_aka_dora=True)
    assert FIVE_RED_PIN in tiles


def test_convert_string_with_aka_dora_as_zero_to_136_array():
    tiles = TilesConverter.string_to_136_array(man="22444", pin="333067", sou="444", has_aka_dora=True)
    assert FIVE_RED_PIN in tiles


def test_one_line_string_to_136_array():
    initial_string = "789m456p555s11222z"
    tiles = TilesConverter.one_line_string_to_136_array(initial_string)
    assert len(tiles) == 14

    new_string = TilesConverter.to_one_line_string(tiles)
    assert initial_string == new_string


def test_one_line_string_to_34_array():
    initial_string = "789m456p555s11222z"
    tiles = TilesConverter.one_line_string_to_34_array(initial_string)
    assert len(tiles) == 34

    tiles = TilesConverter.to_136_array(tiles)
    new_string = TilesConverter.to_one_line_string(tiles)
    assert initial_string == new_string
