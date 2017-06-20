import radix

rtree = radix.Radix()
rnode = rtree.add('1.0.0.0/8')
rnode.data['as'] = '123'
rnode = rtree.add('1.16.0.0/16')
rnode.data['as'] = '234'
rnode = rtree.add('1.32.192.0/18')
rnode.data['as'] = '345'
rnode = rtree.add('1.32.255.0/24')
rnode.data['as'] = '456'
for rnode in rtree:
  print rnode.prefix, rnode.data['as']
for delrnode in rtree.nodes():
  prefix = delrnode.prefix
  asnum = delrnode.data['as']
  rtree.delete(delrnode.prefix)
  for rnode in rtree:
    print rnode.prefix, rnode.data['as']
  newnode = rtree.add(prefix)
  newnode.data['as'] = asnum
