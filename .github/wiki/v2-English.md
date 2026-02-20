Python 3.10+ is supported.

The library contains various tools (shanten, agari, hand calculation)
for the Japanese version of mahjong (riichi mahjong).

## Riichi mahjong hands calculation

This package can be used to calculate riichi mahjong hand details (han, fu, yaku, and points).

It supports optional features like:

| Feature | Keyword parameter | Default value |
|---------|-------------------|---------------|
| Disable or enable open tanyao yaku | `has_open_tanyao` | `False` |
| Disable or enable aka dora in the hand | `has_aka_dora` | `False` |
| Disable or enable double yakuman (like suuanko tanki) | `has_double_yakuman` | `True` |
| Upper limit for cumulative han of non-yakuman yaku (counted yakuman / counted sanbaiman / no limit) | `kazoe_limit` | `HandConstants.KAZOE_LIMITED` |
| Support kiriage mangan | `kiriage` | `False` |
| Allow to disable additional +2 fu in open hand (you can make 1-20 hand with that setting) | `fu_for_open_pinfu` | `True` |
| Disable or enable pinfu tsumo | `fu_for_pinfu_tsumo` | `False` |
| Counting renhou as 5 han or yakuman | `renhou_as_yakuman` | `False` |
| Disable or enable Daisharin yakuman | `has_daisharin` | `False` |
| Disable or enable Daisharin in other suits (Daisuurin, Daichikurin) | `has_daisharin_other_suits` | `False` |
| Disable or enable yakuman for dealing into open hands | `has_sashikomi_yakuman` | `False` |
| Limit yakuman calculation to 6 (maximum score 192000) | `limit_to_sextuple_yakuman` | `True` |
| Disable or enable extra yakuman for all honors 7 pairs | `has_daichisei` | `False` |
| Disable or enable paarenchan without any yaku | `paarenchan_needs_yaku` | `True` |

The code was validated on tenhou.net phoenix replays in total on **11,120,125 hands**.

So, we can say that our hand calculator works the same way that tenhou.net hand calculation.

## How to use

Let's calculate how much will cost this hand:

![image](https://user-images.githubusercontent.com/475367/30796350-3d30431a-a204-11e7-99e5-aab144c82f97.png)

### Tanyao hand by ron

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

### How about tsumo?

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

### What if we add open set?

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

### Riichi and Ura dora

Ura dora indicators can be passed via the `ura_dora_indicators` parameter. Ura dora is only counted when the hand won after riichi.

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

Output:

```
10 40
[Menzen Tsumo, Riichi, Tanyao, San Ankou, Dora 2, Ura Dora 3]
```

## Shanten calculation

Shanten number indicates how many tiles away a hand is from winning. A value of `0` means tenpai (one tile away), and `-1` means the hand is already complete (agari).

`calculate_shanten` returns the minimum shanten across regular hand, chiitoitsu (seven pairs), and kokushi (thirteen orphans) forms. You can also calculate shanten for each form individually.

```python
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter

# regular hand, 2 shanten
tiles = TilesConverter.string_to_34_array(man='13569', pin='123459', sou='443')
print("Regular hand shanten:", Shanten.calculate_shanten(tiles))

# tenpai (0 shanten, one tile away from winning)
tiles = TilesConverter.string_to_34_array(sou='111345677', pin='11', man='567')
print("Tenpai hand:", Shanten.calculate_shanten(tiles))

# complete hand (-1 shanten, already winning)
tiles = TilesConverter.string_to_34_array(sou='111234567', pin='11', man='567')
print("Complete hand:", Shanten.calculate_shanten(tiles))

# calculate shanten for specific hand forms
tiles = TilesConverter.string_to_34_array(sou='114477', pin='114477', man='76')
print("Chiitoitsu shanten:", Shanten.calculate_shanten_for_chiitoitsu_hand(tiles))

tiles = TilesConverter.string_to_34_array(sou='129', pin='19', man='19', honors='1234567')
print("Kokushi shanten:", Shanten.calculate_shanten_for_kokushi_hand(tiles))
```

Output:

```
Regular hand shanten: 2
Tenpai hand: 0
Complete hand: -1
Chiitoitsu shanten: 0
Kokushi shanten: 0
```

## Agari (winning hand detection)

Agari check determines whether the given tiles form a complete hand structure (4 melds + 1 pair, seven pairs, or thirteen orphans). It only validates the tile arrangement, not yaku or scoring.

```python
from mahjong.agari import Agari
from mahjong.tile import TilesConverter

# complete hand: 123s 456s 789s 123p 33m
tiles = TilesConverter.string_to_34_array(sou='123456789', pin='123', man='33')
print("Regular hand:", Agari.is_agari(tiles))

# incomplete hand: 123s 456s 789s 12345p
tiles = TilesConverter.string_to_34_array(sou='123456789', pin='12345')
print("Incomplete hand:", Agari.is_agari(tiles))

# seven pairs (chiitoitsu): 1133557799s 1199p
tiles = TilesConverter.string_to_34_array(sou='1133557799', pin='1199')
print("Seven pairs:", Agari.is_agari(tiles))

# thirteen orphans (kokushi): 19s 19p 199m 1234567z
tiles = TilesConverter.string_to_34_array(sou='19', pin='19', man='199', honors='1234567')
print("Kokushi:", Agari.is_agari(tiles))

# open hand with kan meld: 1111m 123456789p 22s
tiles = TilesConverter.string_to_34_array(man='1111', pin='123456789', sou='22')
open_set = [0, 0, 0, 0]  # kan of 1m (tile index 0 in 34-tile format)
print("Open hand with kan:", Agari.is_agari(tiles, [open_set]))
```

Output:

```
Regular hand: True
Incomplete hand: False
Seven pairs: True
Kokushi: True
Open hand with kan: True
```

## Aotenjou scoring rules

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
