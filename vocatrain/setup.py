import setuptools


with open("../README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vocabulary-trainer-cerobotics",
    version="0.0.1",
    author="Christian Ehrmann",
    author_email="author@example.com",
    description="A basic vocabulary trainer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cerobotics/vocabulary_trainer.git",
    packages=setuptools.find_packages(),
    entry_points={
        'startVocabularyGUI': [],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
