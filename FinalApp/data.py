from .domain import (
  TLecture,
  lecture,
  Department,
  Instructor,
  MeetingTime,
  Room,
  Day,
  
  Teacher_Constrains
)
from .models import (ClassRoom,ClassType,Teacher,Constrains,
Lecture,SharedTeacher,SemesterSubject,Level,Group,Specialization)

class Data(object):
  def __init__(self,department):
    self.ClassRooms = None
    self.LabRooms = None

    self.teachers =None
    self.lectures = []
    self.dept = department
    self.meeting_times = None
    self.number_of_lectures = None
    self.days=None
    self.Teacher_Constrains=None
    self.Levels=None
    

    self.initialize()
  
  def initialize(self):
    # create rooms
   



    #self.ClassRooms = list(ClassRoom.objects.filter(DepartmentId=self.dept.Id))
    self.ClassRooms = list(ClassRoom.objects.filter(ClassTypeId=ClassType.objects.get(Name='Normal')))
    self.LabRooms = list(ClassRoom.objects.filter(ClassTypeId=ClassType.objects.get(Name='Lab')))


    #self.ClassRooms = list(ClassRoom.objects.all())


    # create meeting times
    if self.dept.period=='am':
      meeting_time1 ="08:00 - 10:00"
      meeting_time2 ="10:00 - 12:00"
      meeting_time3 ="12:00 - 2:00"
    else:
      meeting_time1 ="2:00 - 4:00"
      meeting_time2 ="4:00 - 6:00"
      meeting_time3 ="6:00 - 8:00"
    self.meeting_times = [
      meeting_time1, 
      meeting_time2, 
      meeting_time3    ]
  
    self.days=["Sunday","Monday","Tuesday","Wednesday","Thursday"]
    
    

    # creating instructors 
    
    self.teachers = list(Teacher.objects.filter(DepartmentId=self.dept))+list(Teacher.objects.filter(id__in=SharedTeacher.objects.filter(DepartmensId=self.dept).values('TeacherId')))
    
    #Constrains
    
    self.Teacher_Constrains=Constrains.objects.filter(TeacherId__in=self.teachers)

    #create level
   
    self.Levels=list(Level.objects.filter(DepartmentId=self.dept))
    #create groups
    # create courses
    #self.lectures=list(Lecture.objects.filter(DepartmentId=self.dept.Id))
    for lec in Lecture.objects.filter(DepartmentId=self.dept.Id):
        self.lectures.append(lecture(id=lec.id,subject=SemesterSubject.objects.get(id=lec.SubjectId.id), level=Level.objects.get(id=lec.LevelId.id),teachers=Teacher.objects.get(id=lec.TeacherId.id),groups=Group.objects.get(id=lec.GroupId.id) if lec.GroupId!=None else None,specializations=Specialization.objects.get(id=lec.SpecId.id) if lec.SpecId!=None else None))
   
    #self.lectures=(list(Lecture.objects.filter(DepartmentId=self.dept.Id)))

    # create departments
    # define the number of lectures
    self.number_of_lectures = len(self.lectures)
