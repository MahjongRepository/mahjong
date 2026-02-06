Python 3.10以上に対応しています。

本ライブラリには日本麻雀（立直麻雀）用の様々なツール（シャンテン数計算、和了判定、点数計算）が含まれています。

## 立直麻雀の点数計算

本パッケージは立直麻雀の手牌詳細（飜、符、役、点数）を計算するために使用できます。

以下のオプション機能をサポートしています:

| 機能 | キーワード引数 | デフォルト値 |
|------|----------------|--------------|
| 喰い断を有効にするかどうか | `has_open_tanyao` | `False` |
| 赤ドラを有効にするかどうか | `has_aka_dora` | `False` |
| ダブル役満（四暗刻単騎など）を有効にするかどうか | `has_double_yakuman` | `True` |
| 数え役満の扱い（役満または三倍満） | `kazoe_limit` | `HandConstants.KAZOE_LIMITED` |
| 切り上げ満貫を有効にするかどうか | `kiriage` | `False` |
| 喰い平和形ロンに2符を追加するかどうか | `fu_for_open_pinfu` | `True` |
| 平和のツモ符を有効にするかどうか | `fu_for_pinfu_tsumo` | `False` |
| 人和を役満とするかどうか（無効の場合は5飜） | `renhou_as_yakuman` | `False` |
| 大車輪（門前清 22334455667788筒）を有効にするかどうか | `has_daisharin` | `False` |
| 色違いの大車輪（索子：大竹林、萬子：大数隣）を有効にするかどうか | `has_daisharin_other_suits` | `False` |
| オープン立直への放銃を役満にするかどうか | `has_sashikomi_yakuman` | `False` |
| 役満複合の上限を6にするかどうか（最高 192000 点） | `limit_to_sextuple_yakuman` | `True` |
| 大七星（字一色七対子）を有効にするかどうか | `has_daichisei` | `False` |
| 八連荘に役が必要かどうか | `paarenchan_needs_yaku` | `True` |

コードはtenhou.net（天鳳）鳳凰卓の牌譜**11,120,125局**で検証済みです。

したがって、本パッケージの手牌計算機は天鳳の手牌計算と同じように動作していることが確認できます。

## 使い方

次の手牌の点数を計算してみましょう:

![image](https://user-images.githubusercontent.com/475367/30796350-3d30431a-a204-11e7-99e5-aab144c82f97.png)

### 断幺九ロン

```python
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld

# we had to use all 14 tiles in that array
tiles = TilesConverter.string_to_136_array(man='22444', pin='333567', sou='444')
win_tile = TilesConverter.string_to_136_array(sou='4')[0]

result = HandCalculator.estimate_hand_value(tiles, win_tile)

print(result.han, result.fu)
print(result.cost['main'])
print(result.yaku)
for fu_item in result.fu_details:
    print(fu_item)
```

Output:

```
1 40
1300
[Tanyao]
{'fu': 30, 'reason': 'base'}
{'fu': 4, 'reason': 'closed_pon'}
{'fu': 4, 'reason': 'closed_pon'}
{'fu': 2, 'reason': 'open_pon'}
```

### ツモの場合

```python
result = HandCalculator.estimate_hand_value(tiles, win_tile, config=HandConfig(is_tsumo=True))

print(result.han, result.fu)
print(result.cost['main'], result.cost['additional'])
print(result.yaku)
for fu_item in result.fu_details:
    print(fu_item)
```

Output:

```
4 40
4000 2000
[Menzen Tsumo, Tanyao, San Ankou]
{'fu': 20, 'reason': 'base'}
{'fu': 4, 'reason': 'closed_pon'}
{'fu': 4, 'reason': 'closed_pon'}
{'fu': 4, 'reason': 'closed_pon'}
{'fu': 2, 'reason': 'tsumo'}
```

### 副露がある場合

```python
from mahjong.hand_calculating.hand_config import OptionalRules

melds = [Meld(meld_type=Meld.PON, tiles=TilesConverter.string_to_136_array(man='444'))]

result = HandCalculator.estimate_hand_value(tiles, win_tile, melds=melds, config=HandConfig(options=OptionalRules(has_open_tanyao=True)))

print(result.han, result.fu)
print(result.cost['main'])
print(result.yaku)
for fu_item in result.fu_details:
    print(fu_item)
```

Output:

```
1 30
1000
[Tanyao]
{'fu': 20, 'reason': 'base'}
{'fu': 4, 'reason': 'closed_pon'}
{'fu': 2, 'reason': 'open_pon'}
{'fu': 2, 'reason': 'open_pon'}
```

### 立直と裏ドラ

裏ドラ表示牌は `ura_dora_indicators` パラメーターで指定できます。裏ドラは立直後の和了の場合のみカウントされます。

```python
tiles = TilesConverter.string_to_136_array(man='22444', pin='333567', sou='444')
win_tile = TilesConverter.string_to_136_array(sou='4')[0]
dora_indicators = TilesConverter.string_to_136_array(man='1')
ura_dora_indicators = TilesConverter.string_to_136_array(pin='2')

result = HandCalculator.estimate_hand_value(
    tiles,
    win_tile,
    dora_indicators=dora_indicators,
    ura_dora_indicators=ura_dora_indicators,
    config=HandConfig(is_riichi=True, is_tsumo=True)
)

print(result.han, result.fu)
print(result.yaku)
```

Output:

```
10 40
[Menzen Tsumo, Riichi, Tanyao, San Ankou, Dora 2, Ura Dora 3]
```

## シャンテン数計算

```python
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

tiles = TilesConverter.string_to_34_array(man='13569', pin='123459', sou='443')
result = Shanten.calculate_shanten(tiles)

print(result)
```

Output:

```
2
```

## 青天井ルール

```python
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.hand_calculating.scores import Aotenjou
from mahjong.tile import TilesConverter
from mahjong.meld import Meld
from mahjong.constants import EAST

tiles = TilesConverter.string_to_136_array(honors='111133555566667777')
win_tile = TilesConverter.string_to_136_array(honors='3')[0]

melds = [
    Meld(meld_type=Meld.KAN, tiles=TilesConverter.string_to_136_array(honors='1111'), opened=False),
    Meld(meld_type=Meld.KAN, tiles=TilesConverter.string_to_136_array(honors='5555'), opened=False),
    Meld(meld_type=Meld.KAN, tiles=TilesConverter.string_to_136_array(honors='6666'), opened=False),
    Meld(meld_type=Meld.KAN, tiles=TilesConverter.string_to_136_array(honors='7777'), opened=False),
]

result = HandCalculator.estimate_hand_value(
    tiles,
    win_tile,
    melds=melds,
    dora_indicators=TilesConverter.string_to_136_array(honors='4444'),
    ura_dora_indicators=TilesConverter.string_to_136_array(honors='7777'),
    scores_calculator_factory=Aotenjou,
    config=HandConfig(
        is_riichi=True,
        is_tsumo=True,
        is_ippatsu=True,
        is_haitei=True,
        player_wind=EAST,
        round_wind=EAST
    )
)

print(result.han, result.fu)
print(result.cost['main'])
print(result.yaku)
for fu_item in result.fu_details:
    print(fu_item)
```

Output:

```
103 160
12980742146337069071326240823050300
[Menzen Tsumo, Riichi, Ippatsu, Haitei Raoyue, Yakuhai (seat wind east), Yakuhai (round wind east), Daisangen, Suu Kantsu, Tsuu Iisou, Suu Ankou Tanki, Dora 16, Ura Dora 16]
{'fu': 32, 'reason': 'closed_terminal_kan'}
{'fu': 32, 'reason': 'closed_terminal_kan'}
{'fu': 32, 'reason': 'closed_terminal_kan'}
{'fu': 32, 'reason': 'closed_terminal_kan'}
{'fu': 20, 'reason': 'base'}
{'fu': 2, 'reason': 'pair_wait'}
{'fu': 2, 'reason': 'tsumo'}
```
