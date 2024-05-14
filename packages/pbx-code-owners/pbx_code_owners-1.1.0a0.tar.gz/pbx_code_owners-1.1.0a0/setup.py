from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pbx-code-owners",
    version="1.1.0a0",
    packages=find_packages(exclude=["tests*"]),
    url="https://getprintbox.com/",
    license="",
    author="",
    author_email="",
    description="Code Owners implementation",
    install_requires=[
        "pyyaml",
        "requests",
    ],
    extras_require={},
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pbx-code-owners=code_owners:main",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
