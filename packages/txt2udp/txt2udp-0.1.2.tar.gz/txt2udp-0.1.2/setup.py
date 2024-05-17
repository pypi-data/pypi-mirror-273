from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="txt2udp",
    version="0.1.2",
    description="A simple tool for forwarding UDP datagrams through a text-only protocol/interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mirrorange/TXT2UDP",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "txt2udp = txt2udp.main:main",
            "txt2udp-cli = txt2udp.cli:app",
        ]
    },
    install_requires=[
        "pydantic",
        "pydantic-settings",
        "loguru",
    ],
    extras_require={
        "mitm": ["mitmproxy"],
        "cli": ["typer"],
        "all": ["mitmproxy", "typer"],
    },
    author="Orange",
    author_email="orange@icedeer.net",
    license="Apache-2.0",
)
