from setuptools import setup, find_packages

setup(
    name='printmate',
    version='1.2.8',
    packages=find_packages(),
    install_requires=[
        "colorama"],
    entry_points={
        'console_scripts': [
            'printmate = printmate.__main__:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
