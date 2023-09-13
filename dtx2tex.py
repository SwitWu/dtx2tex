# dtx2tex.py
# Copyright (C) 2023 SiyuWu
# This Python Script is used to strip the documentation lines from .dtx file to form .tex file

import re

# various regular expressions patterns
documentclass_pattern = re.compile(r'^\\documentclass(\[.+\])?\{\w+?\}')
begindocument_pattern = re.compile(r'\\begin\{document\}')
enddocument_pattern   = re.compile(r'\\end\{document\}')
comment_start_pattern = re.compile(r'^%?[ ]*(.*)')
macrocode_pattern     = re.compile(r'^%[ ]{4}(\\(begin|end))\{macrocode\}')
flag_pattern          = re.compile(r'\<(\*|\/)\w+\>')
endinput_pattern      = re.compile(r'^\\endinput')
docinput_pattern      = re.compile(r'\\DocInput\{(\\)?\w+\.dtx\}')

# open the file specified by users
dtx_file_name = input("Please enter the file name of the dtx file (without .dtx): ")
lines = []
with open(f'{dtx_file_name}.dtx', 'r') as f:
  lines = f.readlines()

documentclass_line_number = 0
begindocument_line_number = 0
docinput_line_number      = 0
enddocument_line_number   = 0
endinput_line_number      = 0

# get some special line numbers
i = 0
while(documentclass_pattern.search(lines[i]) == None):
  i = i+1
documentclass_line_number = i

while(begindocument_pattern.search(lines[i]) == None):
  i = i+1
begindocument_line_number = i

while(docinput_pattern.search(lines[i]) == None):
  i = i+1
docinput_line_number = i

while(enddocument_pattern.search(lines[i]) == None):
  i = i+1
enddocument_line_number = i

i = len(lines)
while(endinput_pattern.search(lines[i-1]) == None):
  i = i-1
endinput_line_number = i

print("This is dtx2tex.py used to strip documentation lines from dtx.")
print("Basic information:")
print(f"\\documentclass at line {documentclass_line_number+1}")
print("\\begin{document} at line " + f"{begindocument_line_number+1}")
print("\\end{document} at line " + f"{enddocument_line_number+1}")

with open(f'{dtx_file_name}.tex', 'w') as f:
  for number, line in enumerate(lines):
    if number in range(documentclass_line_number, docinput_line_number): # write the preamble lines and settings between \begin{document} and \DocInput (if any)
      f.write(line)
    if number in range(enddocument_line_number + 3, endinput_line_number-1):
      if (flag_pattern.search(lines[number]) != None): # delete the flag line
        ()
      elif (macrocode_pattern.search(lines[number]) == None): # remove the beginning comment character
        f.write(comment_start_pattern.sub(r'\1', lines[number]))
      else: #  change the macrocode environment into verbatim environment
        f.write(macrocode_pattern.sub(r'\1{verbatim}', lines[number]))
  for number in range(docinput_line_number+1, enddocument_line_number+1): # write lines between \DocInput (excluded) and \end{document} (included)
    f.write(lines[number])

print("Process completed.")
print(f"Output file: {dtx_file_name}.tex")