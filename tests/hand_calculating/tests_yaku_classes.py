import pytest

from tests.utils_for_tests import _string_to_34_tiles

from mahjong.hand_calculating.yaku_list.aka_dora import AkaDora
from mahjong.hand_calculating.yaku_list.chankan import Chankan
from mahjong.hand_calculating.yaku_list.daburu_open_riichi import DaburuOpenRiichi
from mahjong.hand_calculating.yaku_list.daburu_riichi import DaburuRiichi
from mahjong.hand_calculating.yaku_list.dora import Dora
from mahjong.hand_calculating.yaku_list.haitei import Haitei
from mahjong.hand_calculating.yaku_list.houtei import Houtei
from mahjong.hand_calculating.yaku_list.ippatsu import Ippatsu
from mahjong.hand_calculating.yaku_list.nagashi_mangan import NagashiMangan
from mahjong.hand_calculating.yaku_list.open_riichi import OpenRiichi
from mahjong.hand_calculating.yaku_list.pinfu import Pinfu
from mahjong.hand_calculating.yaku_list.renhou import Renhou
from mahjong.hand_calculating.yaku_list.riichi import Riichi
from mahjong.hand_calculating.yaku_list.rinshan import Rinshan
from mahjong.hand_calculating.yaku_list.tsumo import Tsumo
from mahjong.hand_calculating.yaku_list.yakuhai_place import YakuhaiOfPlace
from mahjong.hand_calculating.yaku_list.yakuhai_round import YakuhaiOfRound
from mahjong.hand_calculating.yaku_list.yakuman.chiihou import Chiihou
from mahjong.hand_calculating.yaku_list.yakuman.chuuren_poutou import ChuurenPoutou
from mahjong.hand_calculating.yaku_list.yakuman.daburu_chuuren_poutou import DaburuChuurenPoutou
from mahjong.hand_calculating.yaku_list.yakuman.daburu_kokushi import DaburuKokushiMusou
from mahjong.hand_calculating.yaku_list.yakuman.daisharin import Daisharin
from mahjong.hand_calculating.yaku_list.yakuman.paarenchan import Paarenchan
from mahjong.hand_calculating.yaku_list.yakuman.renhou_yakuman import RenhouYakuman
from mahjong.hand_calculating.yaku_list.yakuman.sashikomi import Sashikomi
from mahjong.hand_calculating.yaku_list.yakuman.suuankou_tanki import SuuankouTanki
from mahjong.hand_calculating.yaku_list.yakuman.tenhou import Tenhou


@pytest.mark.parametrize(
    ("yaku_class", "yaku_id"),
    [
        (Chankan, None),
        (DaburuOpenRiichi, 1),
        (DaburuRiichi, None),
        (Haitei, None),
        (Houtei, None),
        (Ippatsu, None),
        (NagashiMangan, None),
        (OpenRiichi, 1),
        (Pinfu, None),
        (Renhou, None),
        (Riichi, None),
        (Rinshan, None),
        (Tsumo, None),
        (YakuhaiOfPlace, None),
        (YakuhaiOfRound, None),
        (Chiihou, None),
        (DaburuChuurenPoutou, None),
        (DaburuKokushiMusou, None),
        (RenhouYakuman, None),
        (Sashikomi, 1),
        (SuuankouTanki, None),
        (Tenhou, None),
        (AkaDora, None),
        (Dora, None),
        (Paarenchan, 1),
    ],
    ids=lambda val: val.__name__ if isinstance(val, type) else str(val),
)
def test_situational_yaku_is_condition_met_returns_true(yaku_class, yaku_id) -> None:
    """
    Verify situational yaku classes return True from is_condition_met.
    """
    yaku = yaku_class(yaku_id)
    assert yaku.is_condition_met(None) is True


def test_aka_dora_str() -> None:
    """
    Verify AkaDora string representation includes han count.
    """
    yaku = AkaDora()
    assert str(yaku) == "Aka Dora 1"


def test_dora_str() -> None:
    """
    Verify Dora string representation includes han count.
    """
    yaku = Dora()
    assert str(yaku) == "Dora 1"


def test_paarenchan_str() -> None:
    """
    Verify Paarenchan string representation includes count.
    """
    yaku = Paarenchan(yaku_id=1)
    assert str(yaku) == "Paarenchan 0"


def test_paarenchan_str_after_set_count() -> None:
    """
    Verify Paarenchan string representation after setting paarenchan count.
    """
    yaku = Paarenchan(yaku_id=1)
    yaku.set_paarenchan_count(3)
    assert str(yaku) == "Paarenchan 3"


def test_chuuren_poutou_is_condition_met_returns_false_for_wrong_length() -> None:
    """
    Verify ChuuRenPoutou returns False when remaining indices length is not 1.

    The hand uses man tiles (0..8 range) with the pattern 1-1-1-2-3-4-5-6-7-8-9-9-9
    but missing the extra 14th tile that would leave exactly 1 index remaining.
    A 13-tile hand with exactly 1-1-1-2-3-4-5-6-7-8-9-9-9 passes all checks
    but has 0 remaining indices after removal, not 1.
    """
    # hand decomposed into sets: three 1m, one each of 2m-8m, three 9m = 13 tiles
    # after removing two 0s and two 8s and one each of 0-8, nothing remains (length 0, not 1)
    hand = [
        _string_to_34_tiles(man="111"),
        _string_to_34_tiles(man="234"),
        _string_to_34_tiles(man="567"),
        _string_to_34_tiles(man="899"),
        _string_to_34_tiles(man="9"),
    ]
    yaku = ChuurenPoutou()
    assert yaku.is_condition_met(hand) is False


def test_daisharin_is_condition_met_returns_false_for_wrong_tile_counts() -> None:
    """
    Verify Daisharin returns False when tile counts do not match the 2-2-2-2-2-2-2 pattern.

    The hand is a single-suit pin hand (tiles 9..17) but uses tiles that do not form
    seven pairs of consecutive values 2-8.
    """
    # using pairs of 1p-7p instead of 2p-8p
    # this means counts[0]=2 and counts[7]=0, which fails the range(1,8) check
    hand = [
        _string_to_34_tiles(pin="11"),
        _string_to_34_tiles(pin="22"),
        _string_to_34_tiles(pin="33"),
        _string_to_34_tiles(pin="44"),
        _string_to_34_tiles(pin="55"),
        _string_to_34_tiles(pin="66"),
        _string_to_34_tiles(pin="77"),
    ]
    yaku = Daisharin()
    assert yaku.is_condition_met(hand, allow_other_sets=True) is False
