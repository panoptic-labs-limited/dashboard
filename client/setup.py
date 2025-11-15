from setuptools import setup, find_packages

setup(
    name="viz",
    version="0.1.0",
    description="Distributed dashboarding framework with reactive components",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "httpx>=0.28.0",
        "pydantic>=2.0.0",
        "viz-shared>=0.1.0",
    ],
)
