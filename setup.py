from distutils.core import setup
from run_latexdiff.parhelp import *

setup(
    name="run-latexdiff",
    version= '0.1.2',
    description="A python code to create diff.tex between latex documents in a git repo.",
    author="Jinliang Yang <jolyang@ucdavis.edu>",
	author_email="Jinliang Yang <jolyang@ucdavis.edu>",
	#url="",
    license="GPLv3",
    packages=["run_latexdiff"], 
    scripts=["bin/run-latexdiff"],
    long_description=open('README.md').read(),
)
