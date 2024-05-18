from setuptools import setup, find_packages

setup(
    name="igcse",
    version="0.3",
    packages=find_packages(),
    description="A simple Python library for IGCSE Computer Science.",
    author="Shahm Najeeb",
    author_email="Nirt_12023@outlook.com",
    url="https://github.com/DefinetlyNotAI/IG_Python_Library",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="igcse computer science",
    install_requires=[
        'requests>=2.25.1',
    ],
    extras_require={
    },
    python_requires='>=3.6',
)
