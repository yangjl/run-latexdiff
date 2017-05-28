#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Copyright � 2012, Paul Hiemstra <paul@numbertheory.nl>, 
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

import os, os.path, subprocess, tempfile, glob, re, sys
from shutil import move


def runCommand(cmd, stdout = None, stderr = None, cwd = None, ignoredRetCodes = []):
    ''' Runs the command and returns an appropriate string '''
    assert isinstance(ignoredRetCodes, list), "ignoredRetCodes should be a list"
    try:
      retcode = subprocess.call(cmd, stdout = stdout, stderr = stderr, cwd = cwd)
      if retcode == 0 or retcode in ignoredRetCodes:
          message = "OK"
      else:
          message = "failed (retcode: %s)" % retcode
    except OSError, e:
        message = "failed, %s" % e
    return(message)

def latexdiff(old_tex, new_tex, diff_tex = None):
  ''' Run latexdiff for the above input '''
  if returnMultiFiles(old_tex, new_tex)==True:
	checkLatexdiff()
	print "Running latexdiff: %s" % runCommand(("latexdiff","--flatten", old_tex, new_tex), stdout = diff_tex)
  else:
	print "Running latexdiff: %s" % runCommand(("latexdiff", old_tex, new_tex), stdout = diff_tex)
  print "diff stored in %s" % diff_tex.name

def pdflatex(tex_file, log_file = None):
  ''' Run pdflatex on the resulting tex file '''
  print "Running pdflatex: %s" % runCommand(("pdflatex", "-interaction=nonstopmode", tex_file),
                                            stdout = log_file, ignoredRetCodes = [1])


def gitOrHg():
  ''' Determine whether we are in a git or mercurial repository'''
  if os.path.exists(".hg"):
    print "Detected Mercurial repository..."
    git = False
  elif os.path.exists(".git"):
    print "Detected Git repository..."
    git = True
  else:
    print "Error, no Git or Mercurial repository present."
    exit()    
  return git

def dumpLocalFile(f, output_fileobj = None):
  ''' Do not dump from the repository, but dump a local file. '''
  print "Dumping a local file %s: %s" % (f, runCommand(("cat", f), stdout = output_fileobj))

def bibtex(aux_file, log_file = None):
  ''' Run bibtex on the diff.aux file to get working citations '''
  print "Running bibtex: %s" % runCommand(("bibtex", aux_file), stdout = log_file)

def compileDiffPdf(log_file = None, diff_tex="diff.tex", diff_aux ="diff.aux"):
  ''' Compile diff.pdf based on diff.tex '''
  if not log_file is None:
    log_file = open(log_file, "w")

  pdflatex(diff_tex, log_file)
  bibtex(diff_aux, log_file)
  pdflatex(diff_tex, log_file)
  pdflatex(diff_tex, log_file)
  if not log_file is None:
    log_file.close()

def processCmdlineArgs(old="old.tex", new="new.tex", git = True):
  ''' Process the command line arguments given by the user '''
  old_fileloc = old
  try:
    new_fileloc = new
  except IndexError:
    if git:
      new_fileloc = "HEAD:" + old_fileloc.split(":")[1]  
    else:
      new_fileloc = "tip:" + old_fileloc.split(":")[1]  
  return old_fileloc, new_fileloc
  
def dumpRepositoryVersion2tmp(old_fileloc, new_fileloc, git):
  old_dir = tempfile.mkdtemp()
  new_dir = tempfile.mkdtemp()
  old_texfile = cloneRepository(old_fileloc, old_dir, git)
  new_texfile = cloneRepository(new_fileloc, new_dir, git)
  return old_texfile, new_texfile

def parseFileloc(fileloc):
  return(fileloc.split(":"))

def cloneRepository(fileloc, dest_dir, git):
  if not "local" in fileloc:    
    if git:
      texfile = cloneGitRepository(fileloc, dest_dir)
    else:
      texfile = cloneHgRepository(fileloc, dest_dir)
        
  else:
    print "Using local revision of %s: OK" % fileloc
    texfile = parseFileloc(fileloc)[1]
  return texfile

def cloneGitRepository(git_fileloc, dest_dir):
  rev, gitfile = parseFileloc(git_fileloc)
  devnull = open(os.devnull, "w")
  print "Cloning repository: %s" % (runCommand(("git","clone", ".", dest_dir), stdout = devnull))
  print "Setting the repository to revision %s: %s" % (rev, runCommand(("git","checkout", rev), 
              stdout = devnull, stderr = devnull, cwd = dest_dir))
  devnull.close()
  return "/".join((dest_dir, gitfile))


def createDiffTex(oldfile, newfile, diff_output = "diff.tex", swaplocal = False):
  ''' Produce diff.tex based on the two files in "oldfile" and "newfile" '''
  diff_tex = open(diff_output, "w")
  if swaplocal:
    latexdiff(newfile, oldfile, diff_tex)
  else:
    latexdiff(oldfile, newfile, diff_tex)
  diff_tex.close()
  
def cleanAllNonePDF():
  ''' Delete all diff files that are not a .pdf file '''
  for filename in glob.glob('diff*') :
    if not "pdf" in filename:
      os.remove(filename)   

def extractMultiFile(mainfile):
  '''Search if the document is composed of multiple .tex files and extract names if needed'''
  main_file = open(mainfile, 'r')
  main_text = main_file.read()
  main_file.close()
  sub_files_input = re.findall("input\\{(.*)}", main_text)
  sub_files_include = re.findall("include\\{(.*)}", main_text)
  return sub_files_input, sub_files_include
  
def checkMultiFiles(sub_files_input, sub_files_include):
  '''return True if LATEX document is spread over multiple files, False otherwise'''
  if len(sub_files_input)>0 or len(sub_files_include)>0:
	return True
	
def returnMultiFiles(old_tex, new_tex):
  '''check if either old_tex or new_tex is composed from multiple files'''
  sub_files_input, sub_files_include = extractMultiFile(old_tex)
  if checkMultiFiles(sub_files_input, sub_files_include)==True:
	return True
  else:
	sub_files_input, sub_files_include = extractMultiFile(new_tex)
	if checkMultiFiles(sub_files_input, sub_files_include)==True:
	  return True
	
def checkLatexdiff():
  '''check if latexdiff supports the --flatten argument'''
  proc = subprocess.Popen(('latexdiff','--flatten'),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  output,errors = proc.communicate()
  noFlatten = re.findall("flatten", errors)
  if len(noFlatten)>0:
	print "ABORTING... \n \n Your version of latexdiff does not support documents splitted over multiple files. \n Please update your version of latexdiff. \n"
	sys.exit(0)

def replacePattern(file, pattern, subst):
  '''Replace (in-place) a pattern in a file'''
  fh, abs_path = tempfile.mkstemp()
  new_file = open(abs_path,'w')
  old_file = open(file, 'r')
  old_text = old_file.read()
  old_file.close()
  new_file.write( re.sub(pattern,subst,re.sub(r'(?<!\\)%.*?\n', "", old_text)) )
  new_file.close()
  os.remove(file)
  move(abs_path, file)
  
def removeTrailingNewlines(texfile):
  '''Remove newlines (\n) that are between \DIFadd{ some text } <-- and this final }'''
  regexp = "\r\n\r}"
  sub_text = "\n}\n"
  replacePattern(texfile, regexp, sub_text)
  regexp = "\r\n\r\r}"
  replacePattern(texfile, regexp, sub_text)

