"""Smoke checks run against an installed wheel or sdist, without the source tree."""

import importlib
import pkgutil
import sys
from importlib.metadata import distribution
from pathlib import Path

import mahjong
from mahjong.agari import Agari
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.shanten import Shanten
from mahjong.tile import TilesConverter


def main() -> None:
    """Check installed metadata, imports and a representative hand calculation."""
    package = distribution("mahjong")
    assert package.version == sys.argv[1]
    assert package.metadata["License-Expression"] == "MIT"

    # Fail if the checkout or an editable installation shadows the distribution.
    assert mahjong.__file__ is not None
    installed_path = Path(mahjong.__file__).resolve()
    assert installed_path == Path(str(package.locate_file("mahjong/__init__.py"))).resolve()
    assert installed_path.with_name("py.typed").is_file()

    assert package.files is not None
    licenses = [file for file in package.files if str(file).endswith(".dist-info/licenses/LICENSE.txt")]
    assert len(licenses) == 1
    assert "Permission is hereby granted" in Path(str(package.locate_file(licenses[0]))).read_text(encoding="utf-8")

    # Import every packaged module, including dynamically configured yaku classes.
    for module in pkgutil.walk_packages(mahjong.__path__, prefix="mahjong."):
        importlib.import_module(module.name)

    tiles = TilesConverter.string_to_34_array(sou="123456789", pin="123", man="33")
    assert Agari.is_agari(tiles)
    assert Shanten.calculate_shanten(tiles) == -1

    hand = TilesConverter.string_to_136_array(man="22444", pin="333567", sou="444")
    win_tile = TilesConverter.string_to_136_array(sou="4")[0]
    result = HandCalculator.estimate_hand_value(hand, win_tile, config=HandConfig(is_tsumo=True))
    assert result.error is None
    assert (result.han, result.fu) == (4, 40)
    assert result.cost is not None
    assert result.cost["main"] == 4000


if __name__ == "__main__":
    main()
