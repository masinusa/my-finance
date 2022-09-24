from setuptools import setup, find_packages

setup(
  name='cookbook',
  version='1.0.0',
  description='workbook cookbook',
  author='Michael Spicer',
  author_email='masinusa@gmail.com',
  packages=find_packages(exclude=['test']),
  install_requires=['openpyxl==3.0.10']
)