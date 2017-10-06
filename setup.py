import io
from distutils.core import setup


def get_long_description():
    """Generate a long description from the README file."""
    descr = []
    for fname in ('README.rst',):
        with io.open(fname, encoding='utf-8') as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='mahjong',
    packages=[
        'mahjong',
        'mahjong.hand_calculating',
        'mahjong.hand_calculating.yaku_list',
        'mahjong.hand_calculating.yaku_list.yakuman',
    ],
    version='1.0.6',
    description='Mahjong hands calculation',
    long_description=get_long_description(),
    author='Alexey Lisikhin',
    author_email='lisikhin@gmail.com',
    url='https://github.com/MahjongRepository/mahjong',
    data_files=[('', ['README.rst'])],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
