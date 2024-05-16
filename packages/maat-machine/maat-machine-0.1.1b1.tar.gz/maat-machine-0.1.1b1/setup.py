# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maat_machine', 'maat_machine.model']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=8.24.0,<9.0.0',
 'matplotlib>=3.8.4,<4.0.0',
 'numpy==1.26.4',
 'opencv-python>=4.9.0.80,<5.0.0.0',
 'pandas>=2.2.2,<3.0.0',
 'pillow>=10.3.0,<11.0.0',
 'scikit-learn>=1.4.2,<2.0.0',
 'tensorflow==2.16.1',
 'tqdm>=4.66.4,<5.0.0']

setup_kwargs = {
    'name': 'maat-machine',
    'version': '0.1.1b1',
    'description': 'Yet another package designed to simplify coding for data science and machine learning',
    'long_description': '',
    'author': 'Dmitry Vlasov',
    'author_email': 'dmitry.v.vlasov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.11.9',
}


setup(**setup_kwargs)
