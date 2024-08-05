import json

from tabulate import tabulate
from os import system, path,sys
from .models import Department,Timetable_Lecture,ClassRoom,Timetable,Lecture
from .utils import print_data, print_population_schedules, print_schedule_as_table
class RunTable(object):
 def __init__(self):
   self.POPULATION_SIZE=15 
   self.MUTATION_RATE=0.1 
   self.CROSSOVER_RATE=0.9
   self.TOURNAMENT_SELECTION_SIZE=4  
   self.NUMB_OF_ELITE_SCHEDULES=2 

 def run(self,department):
  global SCHEDULE_NUMBER, CLASS_NO

  from .data import Data
  from .genetic_algorithm import GeneticAlgorithm
  from .population import Population

  generation_number = 0
  data = Data(department)
  _genetic_algorithm = GeneticAlgorithm(data=data)
  _population = Population(size=self.POPULATION_SIZE, data=data).sort_by_fitness()

  '''print_data(data=data)
  print()
  print()
  
  print_population_schedules(population=_population, generation_number=generation_number)
  print_schedule_as_table(data=data, schedule=_population.schedules[0], generation=generation_number)'''

  while _population.schedules[0].fitness != 1.0:
    generation_number += 1
    if generation_number==4:
      break
    _population = _genetic_algorithm.evolve(population=_population).sort_by_fitness()
    '''print_population_schedules(population=_population, generation_number=generation_number)
    print_schedule_as_table(data=data, schedule=_population.schedules[0], generation=generation_number)'''
  timetable=Timetable()
  timetable.DepartmentId=department
  timetable.save()
  for i in _population.schedules[0]._classes:
     lec=Timetable_Lecture() 
     lec.TimetableId=timetable
     lec.LectureId=Lecture.objects.get(id=i.lecture.id)
     lec.ClassRoomId=ClassRoom.objects.get(id=i.room.id)
     lec.Time=i.meeting_time
     lec.Day=i.day
     lec.save()
 '''if __name__ == '__main__' and __package__ is None:
  sys.path.insert(0, path.dirname(path.abspath(__file__)))'''
  #run(Department.objects.get(id='1'))