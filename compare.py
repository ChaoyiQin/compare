#!/usr/bin/env python
import os, re, datetime, radix

def handle(day):
  dir_bgp = "./"
  dir_rpki = "./"
  file_bgp = dir_bgp + "%s.origins" % day.strftime("%Y%m%d")
  file_rpki = dir_rpki + "%s.csv" % day.strftime("%Y%m%d")
  file_result = "./%s.compare" % day.strftime("%Y%m%d")
  rtree = radix.Radix()
  with open(file_result, 'w') as result:
    with open(file_rpki, 'r') as rpki:
      lines = rpki.readlines()
      for i in range(0, len(lines)):
        content = lines[i].strip()
        sep = content.split(',')
        roa = sep[0]
        asnum = sep[1][2:]
        prefix = sep[2]
        
        if len(sep[3]) == 0:
          prefix_sep = prefix.split('/')
          maxlen = int(prefix_sep[1])
        else:
          maxlen = int(sep[3])

        rnode = rtree.add(prefix)
        if rnode.data.has_key('content'):
          rnode.data['content'].append((asnum, maxlen, roa))
        else:
          rnode.data['content'] = [(asnum, maxlen, roa)]

    with open(file_bgp, 'r') as bgp:
      lines = bgp.readlines()
      for i in range(0, len(lines)):
        content = lines[i].strip()
        sep = content.split('\t')
        prefix = sep[0]
        asnum = sep[1]
        iptype = sep[2]
        if iptype == '4':
          pre_sep = prefix.split('/')
          mask = int(pre_sep[1])
          if mask > 7 and mask < 25:
            rnodes = rtree.search_covering(prefix)
            if len(rnodes) == 0:
              result.write("%s,AS%s,Unknown\n" % (prefix, asnum))
            else:
              ifvalid = 0
              for rnode in rnodes: 
                for roa_tup in rnode.data['content']:
                  if asnum == roa_tup[0] and mask <= roa_tup[1]:
                    result.write("%s,AS%s,Valid\n" % (prefix, asnum))
                    ifvalid = 1
                    break
                if ifvalid == 1:
                  break
              if ifvalid == 0:
                result.write("%s,AS%s,Invalid\n" % (prefix, asnum))
#          result.write("%s, %s, %s\n" % (asnum, prefix, iptype))


if __name__ == '__main__':
  begin = datetime.date(2017, 4, 30)
  end = datetime.date(2017, 4, 30)
  for i in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=i)
    handle(day)
