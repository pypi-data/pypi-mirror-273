
from pathlib import Path

from setuptools import setup


setup(
    name='dashtable2',
    packages=[
        'dashtable',
        'dashtable.dashutils',
        'dashtable.data2md',
        'dashtable.data2rst',
        'dashtable.data2simplerst',
        'dashtable.grid2data',
        'dashtable.html2data',
        'dashtable.simple2data',
        'dashtable.data2rst.cell',
        'dashtable.html2data.restructify',
        'dashtable.html2data.restructify.converters'
    ],
    version=Path('version.txt').read_text(encoding='utf-8').strip(),
    description='A library for converting a HTML tables into ASCII tables, rowspan and colspan allowed!',
    long_description=open('README.rst').read(),
    author='doakey3 & gustavklopp & pasaopasen',
    author_email='qtckpuhdsa@gmail.com',
    url='https://github.com/PasaOpasen/dashtable2',
    license='MIT',
)
