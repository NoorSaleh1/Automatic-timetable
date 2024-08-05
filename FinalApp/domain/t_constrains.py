class Teacher_Constrains(object):
  def __init__(self, id, TeacherId,Sun,Mon,Tue,Wed,Thu):
    self.id = id
    self.TeacherId =TeacherId 
    self.Sun=Sun
    self.Mon=Mon
    self.Tue=Tue
    self.Wed=Wed
    self.Thu=Thu

  def __str__(self):
    return self.name