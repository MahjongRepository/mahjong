本软件包支持Python 3.10及以上版本。

本软件包包含日本麻雀（立直麻雀）各种相关计算工具（向听数计算、和牌判定、得点计算等）。

## 立直麻雀得点计算

本软件包可用于计算立直麻雀手牌详情（番数、符数、役种及得点）。

包含以下可选功能：

| 功能 | 关键字参数 | 默认值 |
|------|-----------|--------|
| 有无食断（非门前清断幺九是否成立） | `has_open_tanyao` | `False` |
| 有无红宝牌 | `has_aka_dora` | `False` |
| 有无双倍役满役种（如四暗刻单骑） | `has_double_yakuman` | `True` |
| 非役满役种累计番数上限设置（累计役满/累计三倍满/无限制） | `kazoe_limit` | `HandConstants.KAZOE_LIMITED` |
| 有无切上满贯 | `kiriage` | `False` |
| 非门清平和型食和是否+2符（总计30符） | `fu_for_open_pinfu` | `True` |
| 平和自摸是否仍然+2符（总计30符） | `fu_for_pinfu_tsumo` | `False` |
| 人和是否视为役满（还是只有5番） | `renhou_as_yakuman` | `False` |
| 是否有大车轮役种（门前清22334455667788饼） | `has_daisharin` | `False` |
| 是否有其他花色的大车轮役种（索：大竹林，万：大数邻） | `has_daisharin_other_suits` | `False` |
| 放铳开立直是否算役满 | `has_sashikomi_yakuman` | `False` |
| 多倍役满是否上限为6倍（最高得点192000） | `limit_to_sextuple_yakuman` | `True` |
| 是否有大七星役满役种（字一色七对子） | `has_daichisei` | `False` |
| 八连庄是否需要有役才能成立 | `paarenchan_needs_yaku` | `True` |

本软件包经过tenhou.net（天凤）**11,120,125局**凤凰对局测试验证。

因此，我们可以确定所提供的算法与天凤算法一致。

## 如何使用

我们来计算一下下面这手牌的得点：

![image](https://user-images.githubusercontent.com/475367/30796350-3d30431a-a204-11e7-99e5-aab144c82f97.png)

### 断幺九荣和

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

输出：

```
1 40
1300
[Tanyao]
{'fu': 30, 'reason': 'base'}
{'fu': 4, 'reason': 'closed_pon'}
{'fu': 4, 'reason': 'closed_pon'}
{'fu': 2, 'reason': 'open_pon'}
```

### 如果是自摸呢？

```python
result = HandCalculator.estimate_hand_value(tiles, win_tile, config=HandConfig(is_tsumo=True))

print(result.han, result.fu)
print(result.cost['main'], result.cost['additional'])
print(result.yaku)
for fu_item in result.fu_details:
    print(fu_item)
```

输出：

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

### 如果有副露又会如何？

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

输出：

```
1 30
1000
[Tanyao]
{'fu': 20, 'reason': 'base'}
{'fu': 4, 'reason': 'closed_pon'}
{'fu': 2, 'reason': 'open_pon'}
{'fu': 2, 'reason': 'open_pon'}
```

### 立直与里宝牌

可以通过 `ura_dora_indicators` 参数传递里宝牌指示牌。里宝牌仅在立直和牌时计算。

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
    config=HandConfig(is_riichi=True, is_tsumo=True),
)

print(result.han, result.fu)
print(result.yaku)
```

输出：

```
10 40
[Menzen Tsumo, Riichi, Tanyao, San Ankou, Dora 2, Ura Dora 3]
```

## 向听数计算

向听数表示手牌距离和牌还差多少张牌。`0` 表示听牌（差一张即可和牌），`-1` 表示手牌已经和牌（完成形）。

`calculate_shanten` 会计算一般形、七对子和国士无双三种形式的向听数，并返回最小值。也可以单独计算每种形式的向听数。

```python
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

# 一般形，2向听
tiles = TilesConverter.string_to_34_array(man='13569', pin='123459', sou='443')
print("一般形向听数:", Shanten.calculate_shanten(tiles))

# 听牌（0向听，差一张即可和牌）
tiles = TilesConverter.string_to_34_array(sou='111345677', pin='11', man='567')
print("听牌:", Shanten.calculate_shanten(tiles))

# 和牌形（-1向听，已经完成）
tiles = TilesConverter.string_to_34_array(sou='111234567', pin='11', man='567')
print("和牌形:", Shanten.calculate_shanten(tiles))

# 单独计算特定形式的向听数
tiles = TilesConverter.string_to_34_array(sou='114477', pin='114477', man='76')
print("七对子向听数:", Shanten.calculate_shanten_for_chiitoitsu_hand(tiles))

tiles = TilesConverter.string_to_34_array(sou='129', pin='19', man='19', honors='1234567')
print("国士无双向听数:", Shanten.calculate_shanten_for_kokushi_hand(tiles))
```

输出：

```
一般形向听数: 2
听牌: 0
和牌形: -1
七对子向听数: 0
国士无双向听数: 0
```

## 和牌判定

和牌判定检查给定的手牌是否构成完成形（4面子1雀头、七对子或国士无双）。此功能仅验证牌的组合结构，不判断役种或点数。

```python
from mahjong.agari import Agari
from mahjong.tile import TilesConverter

# 完成形：123s 456s 789s 123p 33m
tiles = TilesConverter.string_to_34_array(sou='123456789', pin='123', man='33')
print("一般形:", Agari.is_agari(tiles))

# 未完成形：123s 456s 789s 12345p
tiles = TilesConverter.string_to_34_array(sou='123456789', pin='12345')
print("未完成形:", Agari.is_agari(tiles))

# 七对子：1133557799s 1199p
tiles = TilesConverter.string_to_34_array(sou='1133557799', pin='1199')
print("七对子:", Agari.is_agari(tiles))

# 国士无双：19s 19p 199m 1234567z
tiles = TilesConverter.string_to_34_array(sou='19', pin='19', man='199', honors='1234567')
print("国士无双:", Agari.is_agari(tiles))

# 副露手（杠子）：1111m 123456789p 22s
tiles = TilesConverter.string_to_34_array(man='1111', pin='123456789', sou='22')
open_set = [0, 0, 0, 0]  # 一万的杠子（34牌格式中索引为0）
print("副露手（杠子）:", Agari.is_agari(tiles, [open_set]))
```

输出：

```
一般形: True
未完成形: False
七对子: True
国士无双: True
副露手（杠子）: True
```

## 青天井规则

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
        round_wind=EAST,
    ),
)

print(result.han, result.fu)
print(result.cost['main'])
print(result.yaku)
for fu_item in result.fu_details:
    print(fu_item)
```

输出：

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
