from setuptools import setup

import pathlib
import pkg_resources

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name="gator",
    description="The best static site generator you'll ever see",
    version="0.0.1",
    url="https://github.com/kylediaz/gator",
    author="Kyle Diaz",
    author_email="dev@kylediaz.com",
    scripts=["scripts/gator"],
    entry_points={
        'console_scripts': [
            'gator=gator.__main__:main'
        ]
    },
    packages=["gator", "gator.grammar"],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    install_requires=install_requires,
)
