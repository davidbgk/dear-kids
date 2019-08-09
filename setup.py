from setuptools import setup

requires = ["commonmark", "jinja2", "parse-accept-language", "roll", "uvloop"]

setup(
    name="dear-kids",
    version="0.1.0",
    install_requires=requires,
    entry_points={"console_scripts": ["dearkids=dearkids.__main__:run"]},
)
