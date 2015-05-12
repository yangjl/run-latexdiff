
#run-latexdiff

A command line tool to create `latexdiff` pdf's for different git commits. Modified from [scm-latexdiff](https://bitbucket.org/paulhiemstra/scm-latexdiff/overview). All credits go to **scm-latexdiff**.

## INSTALL
This tool uses **distutils** for installation. The following command installs the tool on your machine:
```
python setup.py install
```
To install to a non-standard directory tree (e.g. in your home directory) use **--prefix**:
```
python setup.py install --prefix=/home/spam/
```
Do remember to add **/home/spam/lib/python2.x/site-packages/** to your 
**PYTHONPATH** environment variable.

------------
  
## USAGE:
```
### find help
run-latexdiff --help (or -h)
### running example
run-latexdiff --old OLD:FILE --new NEW:FILE --diff diff.tex
run-latexdiff -o f126:ms/old.tex -n jafo12:ms/new.tex -d ms/diff.tex
```  
### where:
- OLD:    old revision id, **local** for non-commited
- NEW:    new revision id, **local** for non-commited
- FILE:   filename of the file you want to compare

------------

## Notes

- Must run in the directory with **.git** file.
- When referring to a git revision, not the whole sha1 key is needed, you can just provide the first few numbers.
- Multiple tex file may supported but not tested.
- If the tex and its associated file in the subdirectory, just run `pdflatex` manually to generate the pdf file.

-------------------

## License

Copyright © 2012, Paul Hiemstra <paul@numbertheory.nl>, 
Ronald van Haren <ronald@archlinux.org>.
This file is part of scm-latexdiff.

scm-latexdiff is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the Licence, or
(at your option) any later version.

scm-latexdiff is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

