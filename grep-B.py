import sys, os
import re

with open('binary', 'r') as files:
    results = []
    line = files.readline()
    while line:
     results.append(line)
     if line.startswith('Loop time of'):
          value = results[-2].split()[6]
     line = files.readline()
print(value)
