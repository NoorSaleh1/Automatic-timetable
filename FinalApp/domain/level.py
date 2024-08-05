class Level(object):
  def __init__(self,name,number_of_students,number_of_groups,department):
    self.name=name
    self.number_of_students=number_of_students
    self.number_of_groups=number_of_groups
    self.department = department
    
  def __str__(self):
    return self.name
  
  