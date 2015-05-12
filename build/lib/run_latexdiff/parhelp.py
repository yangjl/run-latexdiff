#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

#from __future__ import print_function
from __future__ import division
import sys
import argparse
import textwrap
import os

def getfilenm(diff_tex=""):
    diff = diff_tex.split('.')[0]
    aux = ".".join([diff, "aux"])
    log = ".".join([diff, "log"])
    return aux, log


def myversion(v='0'):
    a0 = '''
    ##########################################################################################
    run-latexdiff version %s
    Modified by Jinliang Yang <jolyang@ucdavis.edu>
    --------------------------------

    # Copyright @ 2012, Paul Hiemstra <paul@numbertheory.nl>,
    # Ronald van Haren <ronald@archlinux.org>.
    # This file is part of scm-latexdiff.

    # scm-latexdiff is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the Licence, or
    # (at your option) any later version.

    # scm-latexdiff is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.
    ##########################################################################################
    ''' % v
    return(a0)


def get_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(myversion(v= "0.1.0"))
        )

    # positional arguments:
    #parser.add_argument('query', metavar='QUERY', type=str, nargs='*', \
    #                    help='the question to answer')

    # optional arguments:
    #parser.add_argument('-p', '--path', help='the path of the input files', \
    #                    nargs='?', default=os.getcwd())
    parser.add_argument('-n','--new', help='new tex file', type=str)

    parser.add_argument('-o','--old', help='old tex file', type=str)

    parser.add_argument('-d', '--diff', help='output diff.tex file', type=str, default="diff.tex")

    return parser
    #parser = get_parser()
    #parser.print_help()

def showHelp(argv):
  ''' Determine whether or not to shows the usage to the user '''
  try:
    old_fileloc = argv[1]
  except IndexError:
    printHelp()
  if old_fileloc in ["-h","h","--help","help","--h"]:
    printHelp()
  if old_fileloc in ["-v","v","--version","-version","version","--v"]:
    import pkg_resources
    print pkg_resources.require("run-latexdiff")[0].version
    exit()

def printHelp():
  ''' Print usage information and quit the program '''
  print '''=============
scm-latexdiff
=============

A command line tool to create diff pdf's from git and mercurial repos.
The script will automatically detect if the repo is git or hg. The
result is a pdf with the differences between the revisions, diff.pdf.

Usage:
  scm-latexdiff OLD:FILE [NEW:FILE]

where:
  OLD:    old revision id, local for non-commited
  NEW:    new revision id, local for non-commited
  FILE:   filename of the file you want to diff


Examples
========

 # for hg
 scm-latexdiff 4:spam.tex
 scm-latexdiff 4:spam.tex 6:spam.tex
 # for git
 scm-latexdiff 87213:spam.tex
 scm-latexdiff 87213:spam.tex 97123:spam.tex
 # You can also diff against non-commited (local) files
 scm-latexdiff local:spam.tex
 scm-latexdiff 2:spam.tex local:spam.tex


Notes
=====

The NEW:FILE argument is optional, default NEW is 'HEAD' when using git,
and 'tip' when using hg. When referring to a git revision, not the whole
sha1 key is needed, you can just provide the first few numbers.


License
=======

Copyright © 2012, Paul Hiemstra <paul@numbertheory.nl>,
Ronald van Haren <ronald@archlinux.org>.

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
'''
  exit()
