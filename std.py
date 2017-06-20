#!/usr/bin/env python

def std():
  std_dict = {('Valid', 'Unknown'): 0, ('Valid', 'Invalid'): 0, ('Unknown', 'Valid'): 0, ('Unknown', 'Invalid'): 0, ('Invalid', 'Valid'): 0, ('Invalid', 'Unknown'): 0}
  with open('result.txt', 'r') as rfile:
    lines = rfile.readlines()
    for line in lines:
      content = line.strip()
      sep = content.split('|')
      left = sep[0].strip()
      lsep = left.split(',')
      lstatus = lsep[-1]
      right = sep[1].strip()
      rsep = right.split(',')
      rstatus = rsep[-1]
      std_dict[(lstatus, rstatus)] += 1
  return std_dict

if __name__ == '__main__':
  result = std()
  print result
