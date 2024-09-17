from setuptools import setup

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
)
