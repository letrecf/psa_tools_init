import sys
import functools as fn
import psa_helpers as aux
from pymongo import MongoClient

DEFAULT_ENC = "utf-8"
MCS_COLLECTION_NAME = "mcs"

def get_value(s,expected):
  hlen=len(expected)
  header=s[:hlen]
  value=s[hlen:]
  if (header != expected):
    print("WARNING: header not found in '%s'" % s.strip())
  else:
    return (value.strip())

def parse_row(s):
  return [i.strip() for i in [s[0:6],s[6:17],s[24:46],s[46:69]]]
  
def read(f):
  skip = lambda x : aux.skip_read(f,x)
  process_value = lambda e:aux.compose(fn.partial(change_encoding,to_enc=DEFAULT_ENC),fn.partial(get_value,expected=e)
  # header
  skip(4)
  prj = process_value("Project    : ")(f.readline())
  # check if result belongs to the expected model
  if prj != self.model:
    print("WARNING: file <%s> is ignored because it belongs to different model '%s'" % (f.name,prj))
    return
  skip(1)
  aname = process_value("Top event  : ")(f.readline())
  skip(2)
  avalue = float(process_value("Frequency = ")(f.readline()))
  skip(4)
  # mcs list
  mcs_count=0
  mcs_list=[]
  while True:
    try:
      sline=aux.change_encoding(f.next(),DEFAULT_ENC)
      if len(sline)==0:
        break
      expr=self.parse_row(sline)
      if expr[0]=="" and expr[2]=="":
        break
      if expr[0]=="":
        mcs_add=filter(None,expr[2:])
      else:
        # new mcs
        mcs_count += 1
        if int(expr[0])==mcs_count:
           current_mcs=mcs()
           current_mcs.position=mcs_count
           current_mcs.value=float(expr[1])
           current_mcs.analysis=aname
           current_mcs.origin=os.path.basename(f.name)
           mcs_list.append(current_mcs)
           mcs_add=filter(None,expr[2:])
        else:
           raise RuntimeError("MCS index is out of sync")
        mcs_list[mcs_count].events+=mcs_add
    except StopIteration:
      break
  # import to db
  client = MongoClient()
  db = client[self.model]
  coll = db[MCS_COLLECTION_NAME]
  for m in mcs_list:
    coll.insert(m.asObj())
  print("--> found %i" % len(mcs_list))
