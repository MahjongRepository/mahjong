本软件包支持Python 3.8及以上版本

若您需要与Python 2兼容，请使用本软件包v1.1.11版本。

本软件包包含日本麻雀（立直麻雀）各种相关计算工具（向听数计算、和牌判定、得点计算等）。

## 立直麻雀得点计算

本软件包可用于计算立直麻雀手牌详情（番数、符数、役种及得点）。

包含以下可选功能：

| 功能 关键 | 字参数 | 默认值 |
| -------- | ---- | ----- |
| 有无食断（非门前清断幺九是否成立） | has_open_tanyao | False
| 有无红宝牌 | has_aka_dora | False
| 有无双倍役满役种（如四暗刻单骑） | has_double_yakuman | True
| 非役满役种累计番数上限设置（累计役满//累计三倍满） | kazoe_limit | HandConstants.KAZOE_LIMITED
| 有无切上满贯 | kiriage | False
| 非门清平和型食和是否+2符（总计30符） | fu_for_open_pinfu | True
| 平和自摸是否仍然+2符（总计30符） | fu_for_pinfu_tsumo | False
| 人和是否视为役满（还是只有5番） | renhou_as_yakuman | False
| 是否有大车轮役种（门前清22334455667788饼） | has_daisharin | False
| 是否有其他花色的大车轮役种（索：大竹林，万：大数邻） | has_daisharin_other_suits | False
| 放铳开立直是否算役满 | has_sashikomi_yakuman | False
| 多倍役满是否上限为6倍 (最高得点192000) | limit_to_sextuple_yakuman | True
| 是否有大七星役满役种（字牌七对子） | has_daichisei | False
| 八连庄是否需要有役才能成立 | paarenchan_needs_yaku | True

本软件包经过tenhou.net（天凤）\**11,120,125 局*\*凤凰对局测试验证

因此，我们可以确定所提供的算法与天凤算法一致。

项目地址: <https://github.com/MahjongRepository/mahjong>

## 如何使用

更多示例请参阅:
<https://github.com/MahjongRepository/mahjong/blob/1x_version/doc/examples.py>

我们来计算一下下面这手牌的得点:

![image](https://user-images.githubusercontent.com/475367/30796350-3d30431a-a204-11e7-99e5-aab144c82f97.png)

### 断幺九荣和

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

输出:

    1 40
    1300
    [Tanyao]
    {'fu': 30, 'reason': 'base'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 2, 'reason': 'open_pon'}

### 如果是自摸呢?

```python
result = calculator.estimate_hand_value(tiles, win_tile, config=HandConfig(is_tsumo=True))

print(result.han, result.fu)
print(result.cost['main'], result.cost['additional'])
print(result.yaku)
for fu_item in result.fu_details:
    print(fu_item)
```

输出:

    4 40
    4000 2000
    [Menzen Tsumo, Tanyao, San Ankou]
    {'fu': 20, 'reason': 'base'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 2, 'reason': 'tsumo'}

### 如果有副露又会如何?

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

    1 30
    1000
    [Tanyao]
    {'fu': 20, 'reason': 'base'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 2, 'reason': 'open_pon'}
    {'fu': 2, 'reason': 'open_pon'}

### 向听数计算

```python
from mahjong.shanten import Shanten

shanten = Shanten()
tiles = TilesConverter.string_to_34_array(man='13569', pin='123459', sou='443')
result = shanten.calculate_shanten(tiles)

print(result)
```

### 青天井规则

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
