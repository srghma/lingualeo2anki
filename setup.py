from setuptools import setup
import os

print(os.environ)

setup(
    name="lingualeo2anki",
    version = "0.0.1",
    author_email="melgaardbjorn@gmail.com",
    entry_points = {
        "console_scripts": [
            "lingualeo2anki = server.__main__:main"
        ]
    },

    test_suite="tests"
)
