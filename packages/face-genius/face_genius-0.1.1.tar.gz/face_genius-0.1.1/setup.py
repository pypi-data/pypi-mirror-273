
from setuptools import setup, find_packages

setup(
    name="face_genius",
    version="0.1.1",
    author="VT",
    author_email="vic.tkachev@gmail.com",
    description="A simple face recognition example package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/victk/face_genius",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    install_requires=[
        "face_recognition",
    ],
)
