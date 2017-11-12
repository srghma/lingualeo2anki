from setuptools import setup
import os

setup(
    name="lingualeo2anki",
    version="0.0.1",
    author='Sergey Homa',
    author_email="melgaardbjorn@gmail.com",
    packages=[
        'server',
    ],
    entry_points={
        "console_scripts": [
            "lingualeo2anki=server.__main__:main"
        ]
    },
    test_suite="tests",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
    ],
    description='Hack lingualeo chrome plugin and save dictionary locally, ready for anki import',
)

