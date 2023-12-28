Python 3.8+ is supported.

If you need Python 2 support you can use v1.1.11 version of the library.

The library contains various tools (shanten, agari, hand calculation)
for the Japanese version of mahjong (riichi mahjong).

## Riichi mahjong hands calculation

It supports optional features like:

| Feature                                                                                      | Keyword parameter              | Default value |
| -------------------------------------------------------------------------------------------- | -------------------------------|---------------|
| Disable or enable open tanyao yaku                                                           | has_open_tanyao              | False
| Disable or enable aka dora in the hand                                                       | has_aka_dora                 | False
| Disable or enable double yakuman (like suuanko tanki)                                        | has_double_yakuman           | True
| Settings for different kazoe yakuman calculation (it сan be an yakuman or a sanbaiman)       | kazoe_limit                  | HandConstants.KAZOE_LIMITED
| Support kiriage mangan                                                                       | kiriage                      | False
| Allow to disable additional +2 fu in open hand (you can make 1-20 hand with that setting)    | fu_for_open_pinfu            | True
| Disable or enable pinfu tsumo                                                                | fu_for_pinfu_tsumo           | False
| Counting renhou as 5 han or yakuman                                                          | renhou_as_yakuman            | False
| Disable or enable Daisharin yakuman                                                          | has_daisharin                | False
| Disable or enable Daisharin in other suits (Daisuurin, Daichikurin)                          | has_daisharin_other_suits    | False
| Disable or enable yakuman for dealing into open hands                                        | has_sashikomi_yakuman        | False
| Limit yakuman calculation to 6 (maximum score 192000)                                        | limit_to_sextuple_yakuman    | True
| Disable or enable extra yakuman for all honors 7 pairs                                       | has_daichisei                | False
| Disable or enable paarenchan without any yaku                                                | paarenchan_needs_yaku        | True

The code was validated on tenhou.net phoenix replays in total on
**11,120,125 hands**.

So, we can say that our hand calculator works the same way that
tenhou.net hand calculation.

## How to use

You can find more examples here: [https://github.com/MahjongRepository/mahjong/blob/1x_version/doc/examples.py](example.py)

Let's calculate how much will cost this hand:

![image](https://user-images.githubusercontent.com/475367/30796350-3d30431a-a204-11e7-99e5-aab144c82f97.png)

### Tanyao hand by ron

```python
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.meld import Meld

calculator = HandCalculator()

# we had to use all 14 tiles in that array
tiles = TilesConverter.string_to_136_array(man='22444', pin='333567', sou='444')
win_tile = TilesConverter.string_to_136_array(sou='4')[0]

result = calculator.estimate_hand_value(tiles, win_tile)

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
result = calculator.estimate_hand_value(tiles, win_tile, config=HandConfig(is_tsumo=True))

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
melds = [Meld(meld_type=Meld.PON, tiles=TilesConverter.string_to_136_array(man='444'))]

result = calculator.estimate_hand_value(tiles, win_tile, melds=melds, config=HandConfig(options=OptionalRules(has_open_tanyao=True)))

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

Shanten calculation
===================

```python
from mahjong.shanten import Shanten

shanten = Shanten()
tiles = TilesConverter.string_to_34_array(man='13569', pin='123459', sou='443')
result = shanten.calculate_shanten(tiles)

print(result)
```

Aotenjou scoring rules
======================

```python
tiles = self.TilesConverter.string_to_136_array(honors='11133555666777')
win_tile = self.TilesConverter.string_to_136_array(honors='3')[0]

melds = [
    Meld(meld_type=Meld.KAN, tiles=TilesConverter.string_to_136_array(honors='1111'), opened=False),
    Meld(meld_type=Meld.KAN, tiles=TilesConverter.string_to_136_array(honors='5555'), opened=False),
    Meld(meld_type=Meld.KAN, tiles=TilesConverter.string_to_136_array(honors='6666'), opened=False),
    Meld(meld_type=Meld.KAN, tiles=TilesConverter.string_to_136_array(honors='7777'), opened=False),
]

result = hand.estimate_hand_value(tiles, win_tile, melds=melds, dora_indicators=TilesConverter.string_to_136_array(honors='44447777'),
    scores_calculator_factory=Aotenjou, config=HandConfig(is_riichi=True, is_tsumo=True, is_ippatsu=True, is_haitei=True, player_wind=EAST, round_wind=EAST))

print(result.han, result.fu)
print(result.cost['main'])
print(result.yaku)
for fu_item in result.fu_details:
    print(fu_item)
```

Output:
```
95 160
50706024009129176059868128215100
[Menzen Tsumo, Riichi, Ippatsu, Haitei Raoyue, Yakuhai (wind of place), Yakuhai (wind of round), Daisangen, Suu kantsu, Tsuu iisou, Suu ankou tanki, Dora 24]
{'fu': 32, 'reason': 'closed_terminal_kan'}
{'fu': 32, 'reason': 'closed_terminal_kan'}
{'fu': 32, 'reason': 'closed_terminal_kan'}
{'fu': 32, 'reason': 'closed_terminal_kan'}
{'fu': 20, 'reason': 'base'}
{'fu': 2, 'reason': 'pair_wait'}
{'fu': 2, 'reason': 'tsumo'}
```
