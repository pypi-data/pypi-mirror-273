# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adtoolbox']

package_data = \
{'': ['*'],
 'adtoolbox': ['pkg_data/.DS_Store',
               'pkg_data/.DS_Store',
               'pkg_data/.DS_Store',
               'pkg_data/.DS_Store',
               'pkg_data/.DS_Store',
               'pkg_data/.DS_Store',
               'pkg_data/.DS_Store',
               'pkg_data/Modified_ADM_Map.json',
               'pkg_data/Modified_ADM_Map.json',
               'pkg_data/Modified_ADM_Map.json',
               'pkg_data/Modified_ADM_Map.json',
               'pkg_data/Modified_ADM_Map.json',
               'pkg_data/Modified_ADM_Map.json',
               'pkg_data/Modified_ADM_Map.json',
               'pkg_data/Modified_ADM_Model.json',
               'pkg_data/Modified_ADM_Model.json',
               'pkg_data/Modified_ADM_Model.json',
               'pkg_data/Modified_ADM_Model.json',
               'pkg_data/Modified_ADM_Model.json',
               'pkg_data/Modified_ADM_Model.json',
               'pkg_data/Modified_ADM_Model.json',
               'pkg_data/README.md',
               'pkg_data/README.md',
               'pkg_data/README.md',
               'pkg_data/README.md',
               'pkg_data/README.md',
               'pkg_data/README.md',
               'pkg_data/README.md',
               'pkg_data/qiime_template_paired.txt',
               'pkg_data/qiime_template_paired.txt',
               'pkg_data/qiime_template_paired.txt',
               'pkg_data/qiime_template_paired.txt',
               'pkg_data/qiime_template_paired.txt',
               'pkg_data/qiime_template_paired.txt',
               'pkg_data/qiime_template_paired.txt',
               'pkg_data/qiime_template_single.txt',
               'pkg_data/qiime_template_single.txt',
               'pkg_data/qiime_template_single.txt',
               'pkg_data/qiime_template_single.txt',
               'pkg_data/qiime_template_single.txt',
               'pkg_data/qiime_template_single.txt',
               'pkg_data/qiime_template_single.txt',
               'pkg_data/slurm_template.txt',
               'pkg_data/slurm_template.txt',
               'pkg_data/slurm_template.txt',
               'pkg_data/slurm_template.txt',
               'pkg_data/slurm_template.txt',
               'pkg_data/slurm_template.txt',
               'pkg_data/slurm_template.txt']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'dash-bootstrap-components>=1.3.1,<2.0.0',
 'dash-escher>=0.0.4,<0.0.5',
 'dash>=2.4.1,<3.0.0',
 'matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.22.4,<2.0.0',
 'openbox>=0.7.17,<0.8.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.8.0,<6.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.4.4,<13.0.0',
 'scipy>=1.8.1,<2.0.0',
 'sympy>=1.10.1,<2.0.0']

entry_points = \
{'console_scripts': ['ADToolbox = adtoolbox.__main__:main']}

setup_kwargs = {
    'name': 'adtoolbox',
    'version': '0.5.7',
    'description': 'A tool for modeling and optimization of anaerobic digestion process.',
    'long_description': '# Toolbox Overview\nParsa Ghadermazi \nparsa96@colostate.edu\n\nAD Toolbox is developed in Chan Lab at Colorado State University. The main goal of this toolbox is to provide the tools that are useful for modeling and optimization of anaerobic digestion process.\n\nInterested in trying ADToolbox? Run the notebooks on Binder or Colab:\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/chan-csu/ADToolbox/HEAD)\n<a target="_blank" href="https://colab.research.google.com/github/chan-csu/ADToolbox/blob/main/README.md">\n  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>\n</a>\n[![PyPI version](https://badge.fury.io/py/adtoolbox.svg)](https://badge.fury.io/py/adtoolbox)\n\n***NOTE***:Binder implementations don\'t offer escher map functionalities yet.\n\nADToolbox comes with a detailed documentation website. You can access this website using the link below:\n\n** [Full Documentation Here](https://chan-csu.github.io/ADToolbox/) **\n\n\n',
    'author': 'ParsaGhadermazi',
    'author_email': '54489047+ParsaGhadermazi@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
