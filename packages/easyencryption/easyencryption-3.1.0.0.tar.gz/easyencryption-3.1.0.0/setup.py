from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_desc = open("README.md", "r")
long_description = long_desc.read()
version = "3.1.0.0"
print(find_packages(include=['easyencryption']))

setup(
    name='easyencryption',
    version=version,
    description='A very easy way to encrypt data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/BlazenBoi/easyencryption/issues',
    author='Blazen',
    author_email='contact@fireballbot.com',
    keywords='',
    packages=find_packages(include=['easyencryption']),
    python_requires='>=3.7',
    install_requires=[
    "setuptools>=42",
    "cryptography",
    "pycryptodomex",
    "pycryptodome",
    "wheel",
    ],
    project_urls={
        'Discord Server': 'https://discord.com/invite/mPU3HybBs9',
        'Bug Tracker': 'https://github.com/BlazenBoi/easyencryption/issues',
        'Source': 'https://github.com/BlazenBoi/easyencryption',
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)
#© 2021 GitHub, Inc.