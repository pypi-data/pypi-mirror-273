import codecs
import os
from setuptools import setup, find_packages

VERSION = '0.2.alpha'
DESCRIPTION = ('ADViewpy is Python Library to visually compare phylogenetic trees')
LONG_DESCRIPTION = 'ADViewpy is Python Library to visually compare phylogenetic trees, utilizing Aggregated Dendrogram for phylogenetic tree visualization. '


setup(
    name="ADViewpy",
    version=VERSION,
    author="Ng Weng Shan",
    author_email="ngwengshan025@hotmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'dendropy',
        'ipycanvas',
        'ipywidgets',
        'scikit-learn',
        'numpy',
        'plotly'
    ],
    keywords=['python', 'phylogenetic tree', 'aggregrated dendrogram','tree comparison'],
    classifiers=["Programming Language :: Python :: 3",
                 "Operating System :: Microsoft :: Windows"]
)
