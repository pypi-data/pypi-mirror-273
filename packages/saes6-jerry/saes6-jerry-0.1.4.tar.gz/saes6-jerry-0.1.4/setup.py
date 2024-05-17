from setuptools import setup, find_packages
from pip._internal.req import parse_requirements

from jerry import __version__

install_reqs = parse_requirements('./requirements.txt', session='dummy')
reqs = [str(ir.requirement) for ir in install_reqs]

setup(
    name='saes6-jerry',
    version=__version__,
    description='SAE S6 Equipe 2 - jerry.',

    url='https://gitlab.com/LennyGonzales/saes6-equipe2-jerry',
    author='GANASSI-GONZALES-SAADI-SAUVA',
    author_email='lenny.gonzales@etu.univ-amu.fr',

    packages=find_packages(),
    install_requires=reqs,
    
    extras_require={},

    entry_points={
        'console_scripts': [
            'saes6-jerry = jerry:main',
        ],
    },

    classifiers=[
        'Intended Audience :: Developers',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)