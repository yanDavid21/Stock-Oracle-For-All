import setuptools

setuptools.setup(
    name="mercury",
    packages=setuptools.find_packages(),
    install_requires=[
        "dagit",
        "dagster",
        "dagster-aws",
        "dagster-postgres",
        "dagster-pandas",
        "dagster-graphql",
        "pandas",
        "pytest",
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
