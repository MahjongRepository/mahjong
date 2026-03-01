TERMINAL_INDICES = frozenset([0, 8, 9, 17, 18, 26])
"""Tile indices (34-format) of terminal tiles — 1 and 9 of each suit (man, pin, sou)."""

EAST = 27
"""Tile index (34-format) for East wind."""

SOUTH = 28
"""Tile index (34-format) for South wind."""

WEST = 29
"""Tile index (34-format) for West wind."""

NORTH = 30
"""Tile index (34-format) for North wind."""

HAKU = 31
"""Tile index (34-format) for Haku (white dragon)."""

HATSU = 32
"""Tile index (34-format) for Hatsu (green dragon)."""

CHUN = 33
"""Tile index (34-format) for Chun (red dragon)."""

WINDS = frozenset([EAST, SOUTH, WEST, NORTH])
"""Tile indices (34-format) of all four wind tiles."""

DRAGONS = frozenset([HAKU, HATSU, CHUN])
"""Tile indices (34-format) of all three dragon tiles."""

HONOR_INDICES = WINDS | DRAGONS
"""Tile indices (34-format) of all honor tiles — winds and dragons."""

TERMINAL_AND_HONOR_INDICES = TERMINAL_INDICES | HONOR_INDICES
"""Tile indices (34-format) of all terminal and honor tiles."""

FIVE_RED_MAN = 16
"""Tile index (136-format) for the red five of man (characters)."""

FIVE_RED_PIN = 52
"""Tile index (136-format) for the red five of pin (circles)."""

FIVE_RED_SOU = 88
"""Tile index (136-format) for the red five of sou (bamboo)."""

AKA_DORAS = frozenset([FIVE_RED_MAN, FIVE_RED_PIN, FIVE_RED_SOU])
"""Tile indices (136-format) of all three red five (aka dora) tiles."""

DISPLAY_WINDS = {EAST: "East", SOUTH: "South", WEST: "West", NORTH: "North"}
"""Mapping from wind tile indices (34-format) to their English display names."""
