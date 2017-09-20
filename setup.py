from distutils.core import setup

description = """
A python module for calculating riichi mahjong hands: yaku, han and fu.

Right now it supports only japanese version (riichi mahjong). MCR (chinese version) in plans

You can find usage examples here https://github.com/MahjongRepository/mahjong
"""

setup(
    name='mahjong',
    packages=[
        'mahjong',
        'mahjong.hand_calculating',
        'mahjong.hand_calculating.yaku_list',
        'mahjong.hand_calculating.yaku_list.yakuman',
    ],
    version='1.0.2',
    description='Mahjong hands calculation',
    long_description=description,
    author='Alexey Lisikhin',
    author_email='lisikhin@gmail.com',
    url='https://github.com/MahjongRepository/mahjong',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
