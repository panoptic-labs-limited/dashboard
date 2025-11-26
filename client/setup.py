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
        "plotly>=5.18.0",
        "pandas>=2.0.0",
        # CLI dependencies
        "click>=8.0.0",
        "rich>=13.0.0",
        "watchdog>=3.0.0",
    ],
    extras_require={
        "altair": ["altair>=5.0.0"],
        "dev": ["pytest>=7.0.0", "black>=23.0.0", "mypy>=1.0.0"],
    },
    entry_points={
        "console_scripts": [
            "streamviz=viz.cli.main:cli",
        ],
    },
)
