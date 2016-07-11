class mcs(object):
  def __init__(self):
    self.analysis=""
    self.position=0
    self.value=0.0
    self.file=""
    self.events=[]

  def asObj(self):
    return self.__dict__
