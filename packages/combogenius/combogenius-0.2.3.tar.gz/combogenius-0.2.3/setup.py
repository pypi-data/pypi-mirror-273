from setuptools import setup, find_packages
from pathlib import Path
this_directory=Path(__file__).parent
long_description=(this_directory / "README.md").read_text()

setup(
    author='Anna Movsisyan, Lusine Aghinyan, Ararat Kazarian, Hovhannes Hovhannisyan, Eduard Petrosyan',
    name='combogenius',
    description='A package designed to efficiently generate new product combinations using check information, and deliver combo suggestions to business partners via email.',
    version='0.2.3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',],
    python_requires='>=3.6',
) 