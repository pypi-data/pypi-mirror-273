#!/usr/bin/env python

from setuptools import setup

def readme():
  with open('README.md', 'r', encoding='utf-8') as f:
    return f.read()


setup(
  name='api5simbiz',
  version='1.0.0',
  author='Sierro',
  author_email='himan.youtube@mail.ru',
  description='Упрощенное взаимодействие с API веб-сайта 5sim.biz',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Gitrer/Fivesimapi',
  packages=['api5simbiz'],
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