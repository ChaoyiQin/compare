#!/usr/bin/env python
import os

def diff():
  os.system('diff -y old20170430.compare 20170430.compare > diff.txt')
  with open('result.txt', 'w') as write:
    with open('diff.txt', 'r') as diff_file:
      lines = diff_file.readlines()
      for line in lines:
        content = line.strip()
        sep = content.split('|')
        if len(sep) > 1:
          write.write(line)

if __name__ == '__main__':
  diff()
