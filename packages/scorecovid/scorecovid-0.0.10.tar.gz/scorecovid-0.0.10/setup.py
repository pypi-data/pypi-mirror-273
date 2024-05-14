import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scorecovid",
    version="0.0.10",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="A package for scoring covid-19 country policies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y-takefuji/score-covid-19-policy",
    project_urls={
        "Bug Tracker": "https://github.com/y-takefuji/score-covid-19-policy",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['scorecovid'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'scorecovid = scorecovid:main'
        ]
    },
)
