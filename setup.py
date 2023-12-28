import setuptools

from distutils.core import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mahjong",
    packages=[
        "mahjong",
        "mahjong.hand_calculating",
        "mahjong.hand_calculating.yaku_list",
        "mahjong.hand_calculating.yaku_list.yakuman",
    ],
    version="1.2.1",
    description="Mahjong hands calculation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Alexey Lisikhin",
    author_email="alexey@nihisil.com",
    url="https://github.com/MahjongRepository/mahjong",
    license='MIT',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
