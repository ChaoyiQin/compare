#!/usr/bin/env python

def merge():
  rpkidict = {}
  with open('old20170430.csv', 'r') as rpki:
    lines = rpki.readlines()
    for line in lines:
      content = line.strip()
      sep = content.split(',')
      roa = sep[0]
      asnum = sep[1]
      prefix = sep[2]
      prefix_sep = prefix.split('/')
      iptype = prefix_sep[0].split('.')
      if len(iptype) < 4:
        continue
      if len(sep[3]) == 0:
        maxlen = int(prefix_sep[1])
      else:
        maxlen = int(sep[3])
      rpkikey = (roa, asnum, prefix, maxlen)
      rpkidict[rpkikey] = 1

  with open('merge20170430.csv', 'w') as rpki:
    for i in rpkidict.keys():
      rpki.write("%s,%s,%s,%s\n" % (i[0], i[1], i[2], i[3]))
        

if __name__ == '__main__':
  merge()
