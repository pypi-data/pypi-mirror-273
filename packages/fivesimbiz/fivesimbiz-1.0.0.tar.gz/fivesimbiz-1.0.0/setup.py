#!/usr/bin/env python

from setuptools import setup

def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()


setup(
  name='fivesimbiz',
  version='1.0.0',
  author='Sierro',
  author_email='himan.youtube@mail.ru',
  description='This library is designed for simplified interaction with the API of the 5sim website',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Gitrer/Fivesimapi',
  packages=['fivesimbiz'],
  install_requires=['requests'],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='example python',
  project_urls={
    'Documentation': 'https://5sim.biz/docs'
  },
  python_requires='>=3.7'
)