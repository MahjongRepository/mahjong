from mahjong.tile import TilesConverter
from mahjong.meld import Meld
from mahjong.hand_calculating.hand_config import HandConfig, OptionalRules
from mahjong.hand_calculating.divider import HandDivider


class TestMixin(object):

    def _string_to_open_34_set(self, sou='', pin='', man='', honors=''):
        open_set = TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)
        open_set[0] //= 4
        open_set[1] //= 4
        open_set[2] //= 4
        return open_set

    def _string_to_34_tile(self, sou='', pin='', man='', honors=''):
        item = TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)
        item[0] //= 4
        return item[0]

    def _string_to_34_array(self, sou='', pin='', man='', honors=''):
        return TilesConverter.string_to_34_array(sou=sou, pin=pin, man=man, honors=honors)

    def _string_to_136_array(self, sou='', pin='', man='', honors=''):
        return TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)

    def _string_to_136_tile(self, sou='', pin='', man='', honors=''):
        return TilesConverter.string_to_136_array(sou=sou, pin=pin, man=man, honors=honors)[0]

    def _to_34_array(self, tiles):
        return TilesConverter.to_34_array(tiles)

    def _to_string(self, tiles_136):
        return TilesConverter.to_one_line_string(tiles_136)

    def _hand(self, tiles, hand_index=0):
        hand_divider = HandDivider()
        return hand_divider.divide_hand(tiles)[hand_index]

    def _make_meld(self, meld_type, is_open=True, man='', pin='', sou='', honors=''):
        tiles = self._string_to_136_array(man=man, pin=pin, sou=sou, honors=honors)
        meld = Meld(meld_type=meld_type, tiles=tiles, opened=is_open, called_tile=tiles[0], who=0)
        return meld

    def _make_hand_config(self,
                          is_tsumo=False,
                          is_riichi=False,
                          is_ippatsu=False,
                          is_rinshan=False,
                          is_chankan=False,
                          is_haitei=False,
                          is_houtei=False,
                          is_daburu_riichi=False,
                          is_nagashi_mangan=False,
                          is_tenhou=False,
                          is_renhou=False,
                          is_chiihou=False,
                          player_wind=None,
                          round_wind=None,
                          has_open_tanyao=False,
                          has_aka_dora=False,
                          disable_double_yakuman=False,
                          renhou_as_yakuman=False,
                          allow_daisharin=False,
                          allow_daisharin_other_suits=False):

        options = OptionalRules(
            has_open_tanyao=has_open_tanyao,
            has_aka_dora=has_aka_dora,
            has_double_yakuman=not disable_double_yakuman,
            renhou_as_yakuman=renhou_as_yakuman,
            has_daisharin=allow_daisharin,
            has_daisharin_other_suits=allow_daisharin_other_suits
        )
        return HandConfig(
            is_tsumo=is_tsumo,
            is_riichi=is_riichi,
            is_ippatsu=is_ippatsu,
            is_rinshan=is_rinshan,
            is_chankan=is_chankan,
            is_haitei=is_haitei,
            is_houtei=is_houtei,
            is_daburu_riichi=is_daburu_riichi,
            is_nagashi_mangan=is_nagashi_mangan,
            is_tenhou=is_tenhou,
            is_renhou=is_renhou,
            is_chiihou=is_chiihou,
            player_wind=player_wind,
            round_wind=round_wind,

            options=options
        )
