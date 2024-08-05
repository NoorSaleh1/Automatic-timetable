class Department(object):
  def __init__(self, name, levels):
    self.name = name
    self.levels=levels

  def __str__(self):
    return self.name
