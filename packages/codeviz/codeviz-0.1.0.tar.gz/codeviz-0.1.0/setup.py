# setup.py

from setuptools import setup, find_packages

setup(
    name='codeviz',
    version='0.1.0',
    description='A code visualization tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/PriyankaKatariya/codeviz',
    author='Priyanka Katariya',
    author_email='priyankatariya.26@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
