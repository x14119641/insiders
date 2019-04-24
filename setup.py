from setuptools import setup


with open('README.md', 'r') as fr:
    long_description = fr.read()

with open('requirements.txt', 'r') as f:
    requirements = f.read()


setup(name='InisdersScraper',
      version='1.0',
      description='Scraper for get insiders data from "gurufocus"',
      author='Dani',
      author_email='daniel.gil.romero24@gmail.com',
      packages=['insiders', ],
      install_requires=requirements,
      url='https://github.com/x14119641/insiders',
      long_description=long_description,
      long_description_content_type="text/markdown",
      license='MIT',
      )
