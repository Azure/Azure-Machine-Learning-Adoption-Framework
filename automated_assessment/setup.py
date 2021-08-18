from codecs import open
from setuptools import setup, find_packages

VERSION = "1.0.0"

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'License :: OSI Approved :: MIT License',
]

DEPENDENCIES = []

setup(
    name='mlclassic',
    version=VERSION,
    description='Azure ML Classic extension',
    long_description='Helps creating an inventory of Azure ML Classic artifacts.',
    license='MIT',
    author='Solliance',
    author_email='ciprian@solliance.net',
    url='https://github.com/solliancenet/microsoft-ml-kinetic',
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    install_requires=DEPENDENCIES
)