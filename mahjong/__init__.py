"""
_summary_.

Tile representation
###################

mpsz-notation
-------------

The *mpsz-notation* is the same format used by the Tenhou (see https://tenhou.net/2/), where each tile is
represented by a two-character string: a digit for the rank followed by a letter for the suit.

The suit letters correspond to:

* `m` - manzu (萬子, characters)
* `p` - pinzu (筒子, circles)
* `s` - souzu (索子, bamboo)
* `z` - jihai (字牌, honors)

Within the numbered suits (`m`, `p`, `s`), ranks run from `1` through `9`; the red fives are
written with rank `0` (e.g., `0m`, `0p`, `0s`).

Honors (`z`) use ranks to distinguish individual tiles:

* `1` - East (東)
* `2` - South (南)
* `3` - West (西)
* `4` - North (北)
* `5` - White dragon (白, haku)
* `6` - Green dragon (發, hatsu)
* `7` - Red dragon (中, chun)

Multiple tiles may be concatenated without separators to form a string that represents a collection. For example:

``123m406p789s11555z``

is equivalent to ``1m2m3m4p0p6p7s8s9s1z1z5z5z5z``.

34-format
---------

In the *34-format*, an entry is assigned to each of the 34 tile types.
It does **not** distinguish a red five from a normal five - both map to the same entry.
The format is commonly used in two ways:

* A sequence of length 34 where each entry represents the count of the corresponding tile type.
* A list of tile-type indices, containing one element per tile rather than counts.
  For example, a pon of 1m is represented as ``[0, 0, 0]``.

The correspondence between the index and the tile is shown in the table below.

+-------+----+----+----+----+----+----+----+----+----+
| Index | 0  | 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  |
+-------+----+----+----+----+----+----+----+----+----+
| Tile  | 1m | 2m | 3m | 4m | 5m | 6m | 7m | 8m | 9m |
+-------+----+----+----+----+----+----+----+----+----+

+-------+----+----+----+----+----+----+----+----+----+
| Index | 9  | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
+-------+----+----+----+----+----+----+----+----+----+
| Tile  | 1p | 2p | 3p | 4p | 5p | 6p | 7p | 8p | 9p |
+-------+----+----+----+----+----+----+----+----+----+

+-------+----+----+----+----+----+----+----+----+----+
| Index | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 |
+-------+----+----+----+----+----+----+----+----+----+
| Tile  | 1s | 2s | 3s | 4s | 5s | 6s | 7s | 8s | 9s |
+-------+----+----+----+----+----+----+----+----+----+

+-------+-----------+------------+-----------+------------+------------+------------+----------+
| Index | 27        | 28         | 29        | 30         | 31         | 32         | 33       |
+-------+-----------+------------+-----------+------------+------------+------------+----------+
| Tile  | East (1z) | South (2z) | West (3z) | North (4z) | White (5z) | Green (6z) | Red (7z) |
+-------+-----------+------------+-----------+------------+------------+------------+----------+

136-format
----------

In the *136-format*, each physical tile (four copies of each of the 34 tile types) is assigned a unique integer.
It is primarily used when treating tiles as individual objects rather than counts, such as melds.

The integers range from 0 to 135.
IDs are assigned in groups of four: the four copies of 1m receive `0`, `1`, `2`, and `3`;
the four copies of 2m receive `4`, `5`, `6`, and `7`;
and so on, up to the four copies of red dragon (7z), which receive `132`, `133`, `134`, and `135`.
Red fives are assigned the indices `16` (`0m`), `52` (`0p`), and `88` (`0s`).
"""
