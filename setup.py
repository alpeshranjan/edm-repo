from setuptools import setup, find_packages

setup(
    name="edm-track-recognizer",
    version="0.1.0",
    description="Identify tracks from continuous EDM/techno mixes using API recognition",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.0",
        "librosa>=0.10.0",
        "soundfile>=0.12.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "tqdm>=4.66.0",
        "pydub>=0.25.1",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
    ],
    entry_points={
        "console_scripts": [
            "edm-recognize=src.cli:main",
        ],
    },
    python_requires=">=3.11",
)

