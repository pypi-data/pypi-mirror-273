# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='sqlman',
    version='0.3.2',
    description='告别SQL语句，python操作mysql的贴心助手',
    url='https://github.com/markadc/sqlman',
    author='WangTuo',
    author_email='markadc@126.com',
    packages=find_packages(),
    license='MIT',
    zip_safe=False,
    install_requires=['DBUtils', 'PyMySQL', 'Faker', 'loguru'],
    keywords=['Python', 'MySQL', 'Database'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
