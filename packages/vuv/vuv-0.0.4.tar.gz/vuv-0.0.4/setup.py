import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vuv",
    version="0.0.4",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="comparing effects on mortality between fully vaccinated and unvaccinated",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/y-takefuji/vuv",
    project_urls={
        "Bug Tracker": "https://github.com/y-takefuji/vuv",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['vuv'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'vuv = vuv:main'
        ]
    },
)
