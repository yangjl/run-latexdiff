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

    USAGE:
    =============
    run-latexdiff -o OLD:FILE -n NEW:FILE --diff

    where:
    OLD:    old revision id, local for non-commited
    NEW:    new revision id, local for non-commited
    FILE:   filename of the file you want to diff
    diff:   output of the diff.tex
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

