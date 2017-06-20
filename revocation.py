#!/usr/bin/env python
import os, re, datetime, radix
import diff, std

def handle(day):
  dir_bgp = "./"
  dir_rpki = "./"
  file_bgp = dir_bgp + "%s.origins" % day.strftime("%Y%m%d")
  file_rpki = dir_rpki + "%s.csv" % day.strftime("%Y%m%d")
  file_result = "./%s.compare" % day.strftime("%Y%m%d")
  rtree = radix.Radix()
  roa_list = []
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

      roa_list.append((roa, asnum, prefix, maxlen))
      rnode = rtree.add(prefix)
      if rnode.data.has_key('content'):
        rnode.data['content'].append((asnum, maxlen, roa))
      else:
        rnode.data['content'] = [(asnum, maxlen, roa)]

  bgp_list = []
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
          bgp_list.append((prefix, asnum, mask))

  times = 0
  with open('stat.txt', 'w') as stat:
    for roa in roa_list:
      prefix = roa[2]
      content = (roa[1], roa[3], roa[0])
      rnode = rtree.search_exact(prefix)
      if rnode:
        rcontent = rnode.data['content']
        if len(rcontent) > 0:
          rcontent.remove(content)
        if len(rcontent) == 0:
          rtree.delete(prefix)
  
      with open(file_result, 'w') as result:
        for i in bgp_list:
          bgp_status = status(i, rtree) 
          if bgp_status == 0:
            result.write("%s,AS%s,Valid\n" % (i[0], i[1]))
          elif bgp_status == 1:
            result.write("%s,AS%s,Unknown\n" % (i[0], i[1]))
          else:
            result.write("%s,AS%s,Invalid\n" % (i[0], i[1]))
  
      rnode = rtree.add(prefix)
      if rnode.data.has_key('content'):
        rnode.data['content'].append(content)
      else:
        rnode.data['content'] = [content]
      diff.diff()
      std_dict = std.std()
      stat.write("(%s,%s,%s):%s\n" % (roa[2], roa[1], roa[3], str(std_dict)))
      times += 1
      if times == 2:
        break
      

    

def status(bgp, rtree):
  prefix = bgp[0]
  asnum = bgp[1]
  mask = bgp[2]
  rnodes = rtree.search_covering(prefix)
  if len(rnodes) == 0:
    return 1
  else:
    for rnode in rnodes: 
      for roa_tup in rnode.data['content']:
        if asnum == roa_tup[0] and mask <= roa_tup[1]:
          return 0
    return 2

if __name__ == '__main__':
  begin = datetime.date(2017, 4, 30)
  end = datetime.date(2017, 4, 30)
  for i in range((end - begin).days + 1):
    day = begin + datetime.timedelta(days=i)
    handle(day)
