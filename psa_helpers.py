import re
import functools as fn
import sys
from __future__ import print_function

def change_encoding(s,to_enc):
  return s.encode(to_enc)

def get_valid_filename(s):
  s=s.strip().replace(" ","_")
  return re.sub(r"(?u)[^-\w]","",s)

def skip_read(f,s):
  for i in range(0,s):
    f.readline()

def get_words(s):
  return re.split("\s+",s)

def compose(*functions):
  return fn.reduce(lambda f,g : lambda x : f(g(x)), reversed(functions),lambda x:x)

def update_progress(progress, prefix=''):
  """ use this helper function to print a progress bar for longer-running scripts.
      The progress value is a value between 0.0 and 1.0. If a prefix is present, it
      will be printed before the progress bar.
  """
  total_length = 40

  if progress == 1.:
    print('\r' + ' '*(total_length + len(prefix) + 50),end='')
    print()
    sys.stdout.flush()
  else:
    bar_length = int(round(total_length*progress))
    print('\r%s [%s%s] %.1f %% ' % (prefix, '='*bar_length, ' '*(total_length-bar_length), progress*100),end='')
    sys.stdout.flush()
