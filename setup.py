import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vk.py",
    version="0.6.0",
    author="prostomarkeloff",
    description="Extremely-fast Python 3.6+ toolkit for create applications work`s with VKAPI. Has bot framework out of-the-box. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prostomarkeloff/vk.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "fast": ["ujson", "uvloop"],
        "ultra": [
            "uvkpy @ https://github.com/prostomarkeloff/uvkpy/archive/master.zip"
        ],
    },
    install_requires=[
        "aiohttp",
        "pydantic",
        "watchgod",
        'async-generator;python_version<"3.7"',
        'contextvars;python_version<"3.7"',
    ],
)
