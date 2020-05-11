.. image:: https://github.com/MahjongRepository/mahjong/workflows/Mahjong%20lib/badge.svg
    :target: https://github.com/MahjongRepository/mahjong

Python 2.7 and 3.5+ are supported.

We support the Japanese version of mahjong only (riichi mahjong).


Riichi mahjong hands calculation
================================

This library can calculate hand cost (han, fu with details, yaku, and scores) for riichi mahjong (Japanese version).

It supports optional features like:

==========================================================================================  ========================= ===========================
Feature                                                                                     Keyword parameter         Default value
==========================================================================================  ========================= ===========================
Disable or enable open tanyao yaku                                                          has_open_tanyao           False
------------------------------------------------------------------------------------------  ------------------------- ---------------------------
Disable or enable aka dora in the hand                                                      has_aka_dora              False
------------------------------------------------------------------------------------------  ------------------------- ---------------------------
Disable or enable double yakuman (like suuanko tanki)                                       has_double_yakuman        True
------------------------------------------------------------------------------------------  ------------------------- ---------------------------
Settings for different kazoe yakuman calculation (it сan be an yakuman or a sanbaiman)      kazoe_limit               HandConstants.KAZOE_LIMITED
------------------------------------------------------------------------------------------  ------------------------- ---------------------------
Support kiriage mangan                                                                      kiriage                   False
------------------------------------------------------------------------------------------  ------------------------- ---------------------------
Allow to disable additional +2 fu in open hand (you can make 1-20 hand with that setting)   fu_for_open_pinfu         True
------------------------------------------------------------------------------------------  ------------------------- ---------------------------
Disable or enable pinfu tsumo                                                               fu_for_pinfu_tsumo        False
------------------------------------------------------------------------------------------  ------------------------- ---------------------------
Counting renhou as 5 han or yakuman                                                         renhou_as_yakuman         False
------------------------------------------------------------------------------------------  ------------------------- ---------------------------
Disable or enable Daisharin yakuman                                                         has_daisharin             False
------------------------------------------------------------------------------------------  ------------------------- ---------------------------
Disable or enable Daisharin in other suits (Daisuurin, Daichikurin)                         has_daisharin_other_suits False
==========================================================================================  ========================= ===========================


The code was validated on tenhou.net phoenix replays in total on **11,120,125 hands**.

So, we can say that our hand calculator works the same way that tenhou.net hand calculation.

Project repository: https://github.com/MahjongRepository/mahjong


How to install
--------------

::

   pip install mahjong


How to use
----------

You can find more examples here: https://github.com/MahjongRepository/mahjong/blob/master/doc/examples.py

Let's calculate how much will cost this hand:

.. image:: https://user-images.githubusercontent.com/475367/30796350-3d30431a-a204-11e7-99e5-aab144c82f97.png


Tanyao hand by ron
^^^^^^^^^^^^^^^^^^

.. code-block:: python

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

Output:

::

    1 40
    1300
    [Tanyao]
    {'fu': 30, 'reason': 'base'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 2, 'reason': 'open_pon'}


How about tsumo?
^^^^^^^^^^^^^^^^

.. code-block:: python

    result = calculator.estimate_hand_value(tiles, win_tile, config=HandConfig(is_tsumo=True))

    print(result.han, result.fu)
    print(result.cost['main'], result.cost['additional'])
    print(result.yaku)
    for fu_item in result.fu_details:
        print(fu_item)

Output:

::

    4 40
    4000 2000
    [Menzen Tsumo, Tanyao, San Ankou]
    {'fu': 20, 'reason': 'base'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 2, 'reason': 'tsumo'}


What if we add open set?
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    melds = [Meld(meld_type=Meld.PON, tiles=TilesConverter.string_to_136_array(man='444'))]

    result = calculator.estimate_hand_value(tiles, win_tile, melds=melds, config=HandConfig(options=OptionalRules(has_open_tanyao=True)))

    print(result.han, result.fu)
    print(result.cost['main'])
    print(result.yaku)
    for fu_item in result.fu_details:
        print(fu_item)

Output:

::

    1 30
    1000
    [Tanyao]
    {'fu': 20, 'reason': 'base'}
    {'fu': 4, 'reason': 'closed_pon'}
    {'fu': 2, 'reason': 'open_pon'}
    {'fu': 2, 'reason': 'open_pon'}


Shanten calculation
===================

.. code-block:: python

    from mahjong.shanten import Shanten

    shanten = Shanten()
    tiles = TilesConverter.string_to_34_array(man='13569', pin='123459', sou='443')
    result = shanten.calculate_shanten(tiles)

    print(result)
