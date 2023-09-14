# dtx2tex.py
# Copyright (C) 2023 SiyuWu
# This Python Script is used to strip the documentation lines from .dtx file to form .tex file

import re

# various regular expressions patterns
documentclass_pattern = re.compile(r'^\\documentclass(\[.+\])?\{\w+?\}')
begindocument_pattern = re.compile(r'\\begin\{document\}')
enddocument_pattern   = re.compile(r'\\end\{document\}')
comment_start_pattern = re.compile(r'^%[ ]?(.*)')
macrocode_pattern     = re.compile(r'^%[ ]{4}(\\(begin|end))\{macrocode\}')
flag_pattern          = re.compile(r'\<(\*|\/)\w+\>')
endinput_pattern      = re.compile(r'^(% )?\\endinput')
docinput_pattern      = re.compile(r'\\DocInput\{(\\)?\w+\.dtx\}')
iffalse_pattern       = re.compile(r'^% \\iffalse.*$')
fi_pattern            = re.compile(r'^% \\fi$')

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
iffalse_line_numbers = []
fi_line_numbers      = []

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

for number in range(len(lines)-1, 0, -1):
  if (endinput_pattern.search(lines[number]) != None):
    endinput_line_number = number

# get all line numbers pairing of '% \iffalse' (with optional ' meta-comment') and '% \fi'
for number in range(endinput_line_number):
  if(iffalse_pattern.search(lines[number]) != None):
    iffalse_line_numbers.append(number)
  # note the second condition, this is because there might exist some \fi corresponding to
  # other type \if... conditions
  if((fi_pattern.search(lines[number]) != None) & (len(fi_line_numbers) < len(iffalse_line_numbers))):
    fi_line_numbers.append(number)
iffalse_fi_pairs_number = len(iffalse_line_numbers)
 

print("This is dtx2tex.py used to strip documentation lines from dtx.")
print("Basic information:")
print("Detecting: "f"\\documentclass at line {documentclass_line_number+1}")
print("Detecting: \\begin{document} at line " + f"{begindocument_line_number+1}")
print("Detecting: \\end{document} at line " + f"{enddocument_line_number+1}")
print("Detecting: \\endinput at line " + f"{endinput_line_number+1}")
print("Detecting: \\iffalse total number " + f"{len(iffalse_line_numbers)}, " "at lines " + f"{[x+1 for x in iffalse_line_numbers]}")
print("Detecting: \\fi total number " + f"{len(fi_line_numbers)} " + "at lines " + f"{[x+1 for x in fi_line_numbers]}")

with open(f'{dtx_file_name}.tex', 'w') as f:
  # write lines between \documentclass (included) and \DocInput (excluded)
  for number in range(documentclass_line_number, docinput_line_number):
    f.write(lines[number])
  # write the body of the documentation (i.e., the part from \DocInput)
  for i in range(iffalse_fi_pairs_number - 1):
    for number in range(fi_line_numbers[i]+1, iffalse_line_numbers[i+1]):
      if (flag_pattern.search(lines[number]) != None): # delete the flag line
        ()
      elif (macrocode_pattern.search(lines[number]) != None): 
        # change the macrocode environment into verbatim environment
        f.write(macrocode_pattern.sub(r'\1{verbatim}', lines[number]))
      elif (comment_start_pattern.search(lines[number]) != None):
        # remove the beginning comment character
        f.write(comment_start_pattern.sub(r'\1', lines[number]))
      else:
        f.write(lines[number])
  for number in range(fi_line_numbers[iffalse_fi_pairs_number - 1] + 1, endinput_line_number):
      if (flag_pattern.search(lines[number]) != None): # delete the flag line
        ()
      elif (macrocode_pattern.search(lines[number]) != None): 
        # change the macrocode environment into verbatim environment
        f.write(macrocode_pattern.sub(r'\1{verbatim}', lines[number]))
      elif (comment_start_pattern.search(lines[number]) != None):
        # remove the beginning comment character
        f.write(comment_start_pattern.sub(r'\1', lines[number]))
      else:
        f.write(lines[number])
  # write lines between \DocInput (excluded) and \end{document} (included)
  for number in range(docinput_line_number+1, enddocument_line_number+1): 
    f.write(lines[number])

print("Process completed.")
print(f"Output file: {dtx_file_name}.tex")
