from .schedule import Schedule

class Population(object):
  def __init__(self, size, data):
    self.schedules = [ Schedule(data).initialize() for _ in range(size)]
    

  def __str__(self):
    return "".join([str(x) for x in self.schedules])

  def sort_by_fitness(self):
    def _sort_schedule(schedule):
        return schedule.fitness
    
    self.schedules = sorted(self.schedules,key=lambda x:_sort_schedule(x),reverse=True)
    
    return self
'''def _sort_schedule(schedule1, schedule2):
      ret_val = 0
      
      if schedule1.fitness > schedule2.fitness:
        ret_val = -1
      elif schedule1.fitness < schedule2.fitness:
        ret_val = 1
      
      return ret_val'''