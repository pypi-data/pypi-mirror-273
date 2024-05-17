# setup.py
from setuptools import setup, find_packages

setup(
    name='trsolucoes',
    version='5.1',
    packages=find_packages(),
    install_requires=[
        'selenium',
    ],
    author='Tainan Ramos',
    author_email='tainan@trsolucoes.com.br',
    description='Uma biblioteca de auxílio para Selenium',
    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    #url='https://github.com/seuusuario/selenium-helper-lib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
