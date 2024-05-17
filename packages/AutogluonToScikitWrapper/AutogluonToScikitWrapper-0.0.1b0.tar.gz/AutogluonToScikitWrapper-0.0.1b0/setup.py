from setuptools import setup, find_packages

VERSION = '0.0.1b'
DESCRIPTION = 'Autogluon to Scikit Wrapper'
LONG_DESCRIPTION = (
    'A wrapper which converts Autogluon models to Scikit-Learn models, '
    'thus breaking any limitation faced by user when implementing Scikit-learn methods to Autogluon Models'
)

# Setting up
setup(
    name="AutogluonToScikitWrapper",
    version=VERSION,
    author="Arijit Singh",
    author_email="arijit@easydata.ai",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["autogluon"],
    keywords=['Autogluon', 'Scikit-learn', 'wrapper'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)