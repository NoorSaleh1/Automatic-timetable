class Group(object):
  def __init__(self, id, name,level,number_of_students):
    self.id = id
    self.name =name 
    self.level=level
    self.number_of_students=number_of_students

  def __str__(self):
    return self.name