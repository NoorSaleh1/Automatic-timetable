from .utils import get_random_number
from copy import deepcopy

from .domain import TLecture 
from .models import (ClassRoom,Department,Teacher,Constrains,
Lecture,SharedTeacher,SemesterSubject,Level,Group,Specialization)


class Schedule(object):
  def __init__(self, data):
    self.data = data
    self._classes = []
    self.class_number =0
    self._fitness =-1
    self.number_of_conflicts=0
    self.is_fitness_changed=True
  
  def __str__(self):
    return "\n".join([str(x) for x in self._classes])

  @property
  def fitness(self):
    if self.is_fitness_changed:
      self._fitness = self.calculate_fitness()
      self.is_fitness_changed = False
    return self._fitness
 
  @property
  def classes(self):
    self.is_fitness_changed = True
    return self._classes
  
  def initialize(self):
    def _create_class(self, lecture):
         if lecture.groups!=None:
            _class = TLecture(id=lecture.id, lecture=lecture)
            self.class_number += 1
            _class.meeting_time =deepcopy(self.data.meeting_times[int(len(self.data.meeting_times) * get_random_number())])
            _class.day=deepcopy(self.data.days[int(len(self.data.days)*get_random_number())])
            _class.room = deepcopy(self.data.LabRooms[int(len(self.data.LabRooms) * get_random_number())])
            self._classes.append(_class)
         else:
            _class = TLecture(id=lecture.id, lecture=lecture)
            self.class_number += 1
            _class.meeting_time = deepcopy(self.data.meeting_times[int(len(self.data.meeting_times) * get_random_number())])
            _class.day=deepcopy(self.data.days[int(len(self.data.days)*get_random_number())])
            _class.room = deepcopy(self.data.ClassRooms[int(len(self.data.ClassRooms) * get_random_number())])
            self._classes.append(_class)
      
    for lec in self.data.lectures:
      _create_class(self,lec)
    return self 
  def calculate_fitness(self):
    number_of_conflicts=0
    for idx, _class in enumerate(self._classes):
      if _class.lecture.specializations!=None and _class.lecture.groups==None:
        if _class.room.seating_capacity<_class.lecture.specializations.number_of_students:
                number_of_conflicts += 1
      elif _class.lecture.groups!=None:
        if _class.room.seating_capacity<_class.lecture.groups.number_of_students:
                number_of_conflicts += 1
      elif _class.room.seating_capacity < _class.lecture.level.number_of_students:
        number_of_conflicts += 1 
      const= Constrains.objects.get(TeacherId=_class.lecture.teachers)         
      if _class.day=='Sunday': 
         if const.Sun==False:
             number_of_conflicts+=1
      elif _class.day=='Monday': 
         if const.Mon==False:
             number_of_conflicts+=1
      elif _class.day=='Tuesday': 
         if const.Tue==False:
             number_of_conflicts+=1
      elif _class.day=='Wednesday': 
         if const.Wed==False:
             number_of_conflicts+=1
      elif _class.day=='Thursday': 
         if const.Thu==False:
             number_of_conflicts+=1
      for _tmp_class in self._classes[idx:]:
        if ((_class.day==_tmp_class.day) and (_class.id!=_tmp_class.id)):
         if _class.meeting_time == _tmp_class.meeting_time:
          if _class.room == _tmp_class.room:
            number_of_conflicts += 1
          if _class.lecture.teachers == _tmp_class.lecture.teachers:
            number_of_conflicts += 1 
          if _class.lecture.level.id==_tmp_class.lecture.level.id:
              if _class.lecture.groups==_tmp_class.lecture.groups:
                 number_of_conflicts += 1  
              if ((_class.lecture.groups==None and _tmp_class.lecture.groups!=None)or(_class.lecture.groups!=None and _tmp_class.lecture.groups==None))and(_class.lecture.specializations==_tmp_class.lecture.specializations):
                  number_of_conflicts += 1 
    self.number_of_conflicts = number_of_conflicts
    return (1/(1.0*(self.number_of_conflicts + 1)))
 