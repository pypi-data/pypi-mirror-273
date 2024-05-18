from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name="trsolucoes",
      version="6.0.0",
      license="MIT License",
      author="Tainan Ramos",
      long_description=readme,
      long_description_content_type="text/markdown",
      author_email="tainan@trsolucoes.com.br",
      keywords="trsolucoes",
      description="Um repositório não oficial de funções de auxilio para Selenium",
      packages=['selenium_helper'],
      requires=['selenium'],)