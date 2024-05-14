from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\\n" + fh.read()

setup(
    name="mfprocess",
    version= '1.0.13',  #'0.0.4',   #
    author="Agustin Bustos Barton",
    author_email="agustinbustosbarton@gmail.com",
    description="Data Process",
    url = "https://github.com/agustinbustosbarton/mfprocess",
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy','pandas','pycountry','pyreadstat','openai==0.28.1','dateparser'],
    keywords=['pypi', 'cicd', 'python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows"
    ]
)
