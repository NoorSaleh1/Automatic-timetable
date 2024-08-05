from .models import *
from .serializers import Teacher2Serializer,Student2Serializer,TLectureSerializer,AccountSerializer,ClassRoomSerializer
from datetime import date,datetime,timedelta
from .data import Data
from django.http import HttpResponseForbidden
from django.conf import settings
from django.test.utils import override_settings
from functools import wraps
def info(Role,account):
    if 'Teacher' in Role :
      teacher=Teacher.objects.get(AccountId=account)
      serializer=Teacher2Serializer(teacher)
      return serializer.data
    elif 'Student' in Role:
       student= Student.objects.get(AccountId=account)
       serializer=Student2Serializer(student)
       return serializer.data
    elif 'Admin' in Role:
        serializer=AccountSerializer(account)
        return serializer.data
    else :
       return None


meeting_times = [
    {'Time': "08:00 - 10:00"}, 
    {'Time': "10:00 - 12:00"}, 
     {'Time': "12:00 - 2:00"},
     {'Time': "2:00 - 4:00"},
     {'Time': "4:00 - 6:00"}] 
    
def Empty_ClassRoom(day=date.today().strftime("%A")):
   ClassRooms=[]
   for cls in ClassRoom.objects.all():
        lectures_times=Timetable_Lecture.objects.filter(ClassRoomId=cls,Day=day).values('Time')
        serializer=ClassRoomSerializer(cls)
        ClassRooms.append([serializer.data]+[time['Time'] for time in meeting_times if time not in lectures_times])

   return ClassRooms

def change_lecture(old_lec,new_lec): 
      conflicts=0
      lecture=Lecture.objects.get(id=new_lec.get('LectureId').id)
      class_room=ClassRoom.objects.get(id=new_lec.get('ClassRoomId').id)
      level=Level.objects.get(id=lecture.LevelId.id)
      teacher=Teacher.objects.get(id=lecture.TeacherId.id)
      teacher_const=Constrains.objects.get(TeacherId=teacher)
      if lecture.SpecId!=None and lecture.GroupId==None:
        spec=Specialization.objects.get(id=lecture.SpecId.id)
        if class_room.seating_capacity<spec.number_of_students:
                conflicts+=1
                return('classroom capacity less than students count')
      elif lecture.GroupId!=None:
        group=Group.objects.get(id=lecture.GroupId.id)
        if class_room.seating_capacity<group.number_of_students:
                conflicts+=1

                return('classroom capacity less than students count') 
      elif class_room.seating_capacity < level.number_of_students:
        return('classroom capacity less than students count')           
      if new_lec.get('day')=='Sunday': 
         if teacher_const.Sun=='F':
             conflicts+=1
             return('teacher is not available on Sunday')
      elif new_lec.get('day')=='Monday': 
         if teacher_const.Mon=='F':
             conflicts+=1
             return('teacher is not available on Monday')
      elif new_lec.get('day')=='Tuesday': 
         if teacher_const.Tue=='F':
                 conflicts+=1
                 return('teacher is not available on Tuesday')

      elif new_lec.get('day')=='Wednesday': 
         if teacher_const.Wed=='F':
                 conflicts+=1
                 return('teacher is not available on Wednesday')

      elif new_lec.get('day')=='Thursday': 
         if teacher_const.Thu=='F':
                conflicts+=1
                return('teacher is not available on Thursday')
      
      all_lec=list(Timetable_Lecture.objects.all())
      for tmp_Tlec in all_lec:
        print(new_lec.get('id'))
        if new_lec.get('Day') == tmp_Tlec.Day and new_lec.get('id') != tmp_Tlec.id:
 
         if new_lec.get('Time') == tmp_Tlec.Time :

          # here the check should be updated to name atleast
           if new_lec.get('ClassRoomId') == tmp_Tlec.ClassRoomId:
             conflicts += 1 
             return('classroom is reserved')
           tmp_lec=Lecture.objects.get(id=tmp_Tlec.LectureId.id)
           if teacher == Teacher.objects.get(id=tmp_lec.TeacherId.id):
               conflicts += 1
               return('teacher is not available')
           if new_lec.get('LectureId').LevelId.id==tmp_Tlec.LectureId.LevelId.id:
              if new_lec.get('LectureId').GroupId==tmp_Tlec.LectureId.GroupId:
                 conflicts += 1  
                 return('The  level student have another lecture ')

              if ((new_lec.get('LectureId').GroupId==None and tmp_Tlec.LectureId.GroupId!=None)or(new_lec.get('LectureId').GroupId!=None and tmp_Tlec.LectureId.GroupId==None))and(new_lec.get('LectureId').SpecId==tmp_Tlec.LectureId.SpecId):
                  conflicts += 1 
                  return('The student level have another lecture ')
 
      if conflicts==0:
        
            return('success')
       
           
def allow_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs): 
        if settings.ALLOW_ACCESS:
            return func(*args, **kwargs)
        else:
            return HttpResponseForbidden("Access denied.")
    return wrapper 
    


    