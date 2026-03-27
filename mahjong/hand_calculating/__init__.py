"""
Hand value calculation pipeline.

This subpackage evaluates a winning hand and produces its han, fu, yaku list,
and payment amounts. The calculation flows through several stages:

1. :class:`~mahjong.hand_calculating.divider.HandDivider` decomposes the hand into all
   valid block combinations (4 melds + 1 pair, or 7 pairs for chiitoitsu).
2. :class:`~mahjong.hand_calculating.yaku.Yaku` subclasses test each decomposition for
   matching yaku patterns (e.g., tanyao, pinfu, honitsu).
3. :class:`~mahjong.hand_calculating.fu.FuCalculator` computes minipoints from the meld
   structure, wait type, pair, and winning method.
4. :class:`~mahjong.hand_calculating.scores.ScoresCalculator` converts han and fu into
   payment amounts, accounting for honba and kyoutaku bonuses.

:class:`~mahjong.hand_calculating.hand.HandCalculator` orchestrates the full pipeline and
returns a :class:`~mahjong.hand_calculating.hand_response.HandResponse` with the
highest-scoring result.

Behavior is controlled by :class:`~mahjong.hand_calculating.hand_config.HandConfig`, which
specifies win conditions (tsumo/ron), wind context, and optional rule variants such as
open tanyao, aka dora, and double yakuman.
"""
