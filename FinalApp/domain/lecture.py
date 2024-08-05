class lecture(object):
  def __init__(self, id,subject, level,teachers,groups=None,specializations=None):
    self.id=id
    self.subject=subject
    self.level=level
    self.groups=groups
    self.specializations=specializations
    self.teachers = teachers

  def __str__(self):
    return self.subject.Name

''' LevelId=models.ForeignKey(Level,related_name="Lectures",on_delete=models.CASCADE)
     GroupId=models.ForeignKey(Group,related_name="Lectures",on_delete=models.CASCADE,null=True)
     SpecId=models.ForeignKey(Specialization,related_name="Lectures",on_delete=models.CASCADE,null=True)
     SubjectId=models.ForeignKey(SemesterSubject,related_name="Lectures",on_delete=models.CASCADE)
     TeacherId'''