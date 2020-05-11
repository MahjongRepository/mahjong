import setuptools

from distutils.core import setup


with open('README.rst', 'r') as f:
    readme = f.read()

with open('CHANGELOG.rst', 'r') as f:
    changelog = f.read()

setup(
    name='mahjong',
    packages=[
        'mahjong',
        'mahjong.hand_calculating',
        'mahjong.hand_calculating.yaku_list',
        'mahjong.hand_calculating.yaku_list.yakuman',
    ],
    version='1.1.9',
    description='Mahjong hands calculation',
    long_description=readme + '\n\n' + changelog,
    author='Alexey Lisikhin',
    author_email='lisikhin@gmail.com',
    url='https://github.com/MahjongRepository/mahjong',
    data_files=[('', ['README.rst', 'CHANGELOG.rst'])],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
