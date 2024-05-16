from setuptools import setup, find_packages

setup(
    name='UmiTestData',
    version='0.1',
    packages=find_packages(),
    description='A simple tool to generate random test data',
    author='UmiCore - Kazuya',
    url='https://github.com/kazuya-2006-26',
    license='MIT',
    install_requires=[
        'random',
        'time',
        'json',
        'string',
        'datetime',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)