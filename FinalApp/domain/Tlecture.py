

class TLecture(object):
  def __init__(self, id, lecture,teacher=None,group=None,specialization=None):
    self.id = id
    #self.department = department
    self.lecture = lecture
    self.teacher = teacher
    self.group=group
    self.specialization=specialization
    self.room = None
    self.meeting_time = None
    self.day=None

  def __str__(self):
    _fmt = '[{lecture},{room},{teacher},{meeting_time}]'
    args = {
      #'department': str(self.department),
      'lecture': str(self.lecture),
      'group': str(self.group),
      'specialization':str(self.specialization),
      'room': str(self.room),
      'teacher': str(self.teacher),
      'day':str(self.day),

      'meeting_time': str(self.meeting_time)
    }
    return _fmt.format(**args)
