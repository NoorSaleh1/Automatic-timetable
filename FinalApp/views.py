import ast
from .driver import RunTable
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework import status,filters
from rest_framework.response import Response
from .functions import *
from .driver import *


# Create your views here.
###########################################################Admin###########################################################
#Manage Department
@api_view(['POST','GET'])
def department(request):
        if request.method=='POST':
                Data=json.loads(request.data.get('Department'))
                serializer=DepartmentSerializer(data=Data)
                if serializer.is_valid():
                      #عشان يحفظ اسم القسم كله كابتل
                      data=serializer.validated_data
                      data['Name']=data['Name'].upper()
                      serializer.create(data)   
                      teacherId=json.loads(request.data.get('DM'))['id']
                      
                      dm=DM()
                      dm.DepartmentId=Department.objects.get(Id=Data['Id'])
                      dm.TeacherId=Teacher.objects.get(id=teacherId)
                      dm.save()
                      account=Account.objects.get(id=Teacher.objects.get(id=teacherId).AccountId.id)
                      account.roles.add(Role.objects.get(Name='DM'))
                      return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)            
        elif request.method=='GET':
               Dep=Department.objects.all().order_by('Name')
               map=[]
               for dep in Dep:
                     
                     dm=DM.objects.get(DepartmentId=dep) 
                     map.append({
                          "Department": DepartmentSerializer(dep).data,
                           "DM": DM2Serializer(dm).data,
                           
                           })
               return Response(map)               
@api_view(['GET','PUT','DELETE'])  
def department_PK(request,pk):
      try:
       department=Department.objects.get(Id=pk)
       if request.method=='GET':    
             serializer=DepartmentSerializer(department)
             dm=DM.objects.get(DepartmentId=department)
             DMserializer=DM2Serializer(dm)
             
             map={
                   'Depatment':serializer,
                   'DM':DMserializer
             }
             return Response(map)
       elif request.method=='PUT':
          data=json.loads(request.data.get('Department'))
          
          serializer=DepartmentSerializer(department,data=data)
          if serializer.is_valid() :
            serializer.save()
            data=json.loads(request.data.get('DM'))
            teacherId=data['id']
            dm=DM.objects.get(DepartmentId=department)
            if (dm.TeacherId!=Teacher.objects.get(id=teacherId)):  
              if(DM.objects.filter(TeacherId=dm.TeacherId).count()==1):
                account=Account.objects.get(id=Teacher.objects.get(id=dm.TeacherId.id).AccountId.id)
                account.roles.remove(Role.objects.get(Name='DM'))
              dm.TeacherId=Teacher.objects.get(id=teacherId)
              dm.save()
              if (DM.objects.filter(TeacherId=dm.TeacherId).count()==1):
                 account=Account.objects.get(id=Teacher.objects.get(id=dm.TeacherId.id).AccountId.id)
                 account.roles.add(Role.objects.get(Name='DM'))
            return Response(status=status.HTTP_200_OK)

       elif request.method=='DELETE':
             dm=DM.objects.get(DepartmentId=department)
             account=Account.objects.get(id=Teacher.objects.get(id=dm.TeacherId.id).AccountId.id)
             account.roles.remove(Role.objects.get(Name='DM'))
             department.delete()
             return Response(status=status.HTTP_200_OK)
             
       
      except Department.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#Manage classrooms
@api_view(['POST','GET'])
def classroom(request):
        if request.method=='POST':
                serializer=ClassRoomSerializer(data=request.data)
                if serializer.is_valid():
                      serializer.save()
                      return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)            
        elif request.method=='GET':
               cr=ClassRoom.objects.all().order_by('Name')
               serializer=ClassRoom2Serializer(cr,many=True)

               return Response(serializer.data)               
@api_view(['GET','PUT','DELETE'])  
def classroom_PK(request,pk):
      try:
       classroom=ClassRoom.objects.get(id=pk)

       if request.method=='GET':    
             serializer=ClassRoom2Serializer(classroom)
             
             return Response(serializer.data)
       elif request.method=='PUT':
            serializer=ClassRoomSerializer(classroom,data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(status=status.HTTP_200_OK)

       elif request.method=='DELETE':
             classroom.delete()
             return Response(status=status.HTTP_200_OK)
             
       
      except ClassRoom.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def classType(request):
       if request.method=='GET':
               cr=ClassType.objects.all()
               serializer=ClassTypeSerializer(cr,many=True)

               return Response(serializer.data)   
#Manage student
@api_view(['POST','GET'])
def students(request):
        if request.method=='POST':
                serializer=StudentSerializer(data=request.data[0])
                if serializer.is_valid():
                      serializer.save()
                      serializer=AccountSerializer(data=request.data[1])
                      if serializer.is_valid():
                        serializer.save()
                        return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)            
        elif request.method=='GET':
               CR=Student.objects.all()
               serializer=Student2Serializer(CR,many=True)
               return Response(serializer.data)         
@api_view(['POST','GET'])
def student(request):
        #الريكويست بيكون فيه ليست فيها عنصرين العنصر الأول هو معلومات الطالب والثاني هو الحساب
       #يجب عند إضافة كل طالب أن نزيد عدد الطلاب في القروب والتخصص وعند الحذف برضو
        if request.method=='POST':
                      account_data=json.loads(request.data.get('account'))
                      account=Account()
                      account.Email=account_data['Email']
                      account.Password=account_data['Password']
                      account.save()
                      role=Role.objects.get(id=3)
                      account.roles.add(role)
                      account.save()
                      student_info=json.loads(request.data.get('student'))
                      student=Student()
                      student.Name=student_info['Name']
                      student.LevelId=Level.objects.get(id=student_info['LevelId'])
                      if student_info['SpecializationId']!='0':
                       student.SpecializationId=Specialization.objects.get(id=student_info['SpecializationId'])
                      
                      student.GroupId=Group.objects.get(id=student_info['GroupId'])
                      student.DepartmentId=Department.objects.get(Id=student_info['DepartmentId']) 
                      student.AccountId=account
                      student.save()
                      return Response(status=status.HTTP_201_CREATED)
        elif request.method=='GET':
               CR=Student.objects.all()
               serializer=Student2Serializer(CR,many=True)
               return Response(serializer.data)         

@api_view(['GET','PUT','DELETE'])  
def student_PK(request,pk):
      try:
       student=Student.objects.get(id=pk)
       if request.method=='GET':    
             serializer=Student2Serializer(student)
             return Response(serializer.data)
       elif request.method=='PUT':
            account=Account.objects.get(id=student.AccountId.id)
            stu=json.loads(request.data.get('student'))
            if stu['SpecializationId']!='0':
               Tserializer=StudentSerializer(student,data=stu) 
               Account_data=json.loads(request.data.get('account'))
               if Tserializer.is_valid():
                 Tserializer.save()
                 account.Email=Account_data['Email']
                 account.Password=Account_data['Password']
                 account.save()
                 return Response(status=status.HTTP_200_OK)
               else:
                 return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                 student.AccountId=account
                 student.Name=stu['Name']
                 student.LevelId=Level.objects.get(id=int(stu['LevelId']))
                 student.GroupId=Group.objects.get(id=int(stu['GroupId']))
                 student.SpecializationId=None
                 student.DepartmentId=Department.objects.get(Id=stu['DepartmentId'])
                 student.save()
                 Account_data=json.loads(request.data.get('account'))
                 account.Email=Account_data['Email']
                 account.Password=Account_data['Password']
                 account.save()
                 return Response(status=status.HTTP_200_OK)
                 
            
            

       elif request.method=='DELETE':
             account=Account.objects.get(id=student.AccountId.id)
             student.delete()
             account.delete()
             return Response(status=status.HTTP_200_OK)
             
       
      except Student.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

##########################################################DM##########################################################
#create lecture  
@api_view(['POST']) 
def lecture(request):
        if request.method=='POST':
             data=request.data
             lecture=Lecture()
             lecture.DepartmentId=Department.objects.get(Id=data['DepartmentId'])
             lecture.SubjectId=SemesterSubject.objects.get(id=data['SubjectId'])
             lecture.TeacherId=Teacher.objects.get(id=data['TeacherId'])
             lecture.LevelId=Level.objects.get(id=data['LevelId'])
             if data['SpecId']!='0':
                  lecture.SpecId=Specialization.objects.get(id=data['SpecId'])
             if data['GroupId']!='0':
                  lecture.GroupId=Group.objects.get(id=data['GroupId']) 
             lecture.save()          
             return Response(status=status.HTTP_201_CREATED)  
@api_view(['GET'])  
def get_lectures(request,pk):
         dep=Department.objects.get(Id=pk)
         lec=Lecture.objects.filter(DepartmentId=dep)
         if request.method=='GET':    
             serializer=Lecture2Serializer(lec,many=True)
             return Response(serializer.data)
@api_view(['POST'])  
def create_lectures(request,pk):
      if request.method=='POST':   
         dep=Department.objects.get(Id=pk)
         subject=Subject.objects.filter(DepartmentId=dep)
         sem_subject=SemesterSubject.objects.filter(SubjectId__in=subject)
         teacher=teacher_subject.objects.filter(Subject__in=sem_subject)
         
         for i in teacher:
              lecture=Lecture()
              lecture.DepartmentId=dep
              lecture.SubjectId=i.Subject
              lecture.TeacherId=i.teacher
              lecture.save()
        # lec=Lecture.objects.filter(DepartmentId=dep)
        # serializer=Lecture2Serializer(lec,many=True)
         return Response(status=status.HTTP_201_CREATED)
@api_view(['PUT','DELETE'])  
def lecture_PK(request,pk):
      try:
       lecture=Lecture.objects.get(id=pk)
       if request.method=='PUT':
             data=request.data
             lecture.DepartmentId=Department.objects.get(Id=data['DepartmentId'])
             lecture.SubjectId=SemesterSubject.objects.get(id=data['SubjectId'])
             lecture.TeacherId=Teacher.objects.get(id=data['TeacherId'])
             lecture.LevelId=Level.objects.get(id=data['LevelId'])
             if data['SpecId']!='0':
                  lecture.SpecId=Specialization.objects.get(id=data['SpecId'])
             if data['GroupId']!='0': 
                  lecture.GroupId=Group.objects.get(id=data['GroupId']) 
             lecture.save()          
             return Response(status=status.HTTP_200_OK)
       elif request.method=='DELETE':
             lecture.delete()
             return Response(status=status.HTTP_200_OK)
             
       
      except Lecture.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#DM
@api_view(['GET'])
def get_DM(request,pk):
         teacher=Teacher.objects.get(id=pk)
         dm=DM.objects.filter(TeacherId=teacher)
         if request.method=='GET':    
             serializer=DM2Serializer(dm,many=True)
             return Response(serializer.data)

#create timetable
@api_view(['POST','GET'])
def create_timetable(request,pk):  
       dept=Department.objects.get(Id=pk)
       if request.method=='POST':
                  lectues=Lecture.objects.filter(DepartmentId=dept)
                  if lectues.exists:
                     timetable_exists=Timetable.objects.filter(DepartmentId=dept)
                     if timetable_exists.exists():
                         timetable_exists.delete()
                         try:
                           pub=published.objects.get(DepartmentId=dept)  
                           pub.delete()
                         except:
                              None
                     time_table=RunTable()
                     time_table.run(dept)
                     dm_Notification=DM_Notification()
                     dm_Notification.DMId=dept
                     dm_Notification.Title='the timetable was created'
                     dm_Notification.Content='the timetable was created succefully'
                     dm_Notification.seen=False
                     dm_Notification.date=datetime.now()
                     dm_Notification.save()
                     '''T_lecture=Timetable_Lecture.objects.filter(LectureId__in=lecture)
                     serializer=TLecture2Serializer(T_lecture,many=True)'''
                     return Response(status=status.HTTP_201_CREATED)
                  elif (lectues.count==0):
                        return Response(status=status.HTTP_404_NOT_FOUND)
                  return Response(status=status.HTTP_400_BAD_REQUEST)
       elif request.method=='GET':
                  lecture=list(Lecture.objects.filter(DepartmentId=pk))
                  T_lecture=Timetable_Lecture.objects.filter(LectureId__in=lecture)
                  serializer=TLecture2Serializer(T_lecture,many=True)
                  #! تابعة للنشر وتنحط في حق التعديل برضور
                  Teacher_Notify=Teacher_Notification()
                  Teacher_Notify.DepartmentId=dept
                  Teacher_Notify.Content='Your time table for this semester is created'
                  Teacher_Notify.date=datetime.now()
                  Teacher_Notify.seen=False
                  Teacher_Notify.save()
                  Student_Notify=Student_Notification()
                  Student_Notify.DepartmentId=dept
                  Student_Notify.Content='Your time table for this semester is created'
                  Student_Notify.date=datetime.now()
                  Student_Notify.seen=False
                  Student_Notify.save()

                  return Response(serializer.data)
#!neeeeeeeeeeew
@api_view(['GET'])
def get_timetable(request,pk):
       dept=Department.objects.get(Id=pk)
       if request.method=='GET':
                 try:
                  T_lecture=Timetable.objects.get(DepartmentId=dept)
                 
                  return Response({'bool':True})
                 except:
                      return Response({'bool':False})
 
@api_view(['GET'])
def level_timetable(request,pk,Lpk):
       dept=Department.objects.get(Id=pk)
       level=Level.objects.get(id=Lpk)if Lpk!=0 else Level.objects.filter(DepartmentId=dept).order_by('Name').first()
       if request.method=='GET':
                  lecture=Lecture.objects.filter(DepartmentId=dept,LevelId=level)

                  T_lecture=Timetable_Lecture.objects.filter(LectureId__in=lecture)
                  serializer=TLecture2Serializer(T_lecture,many=True)
                  return Response(serializer.data)
                  
@api_view(['PUT','DELETE'])   
def timetable(request,pk):
      try:        
            if request.method=='PUT':
                  T_lecture=Timetable_Lecture.objects.get(id=int(pk))
                  serializer=TLectureSerializer(data=request.data)
                  if serializer.is_valid():         
                    print(serializer.validated_data)
                    result=change_lecture(T_lecture,serializer.validated_data)
                    print(result)
                    map={'message':result}
                    if result=='success':    
                       serializer=TLectureSerializer(T_lecture,data=request.data)
                       if serializer.is_valid(): 
                            serializer.save()
                            return Response(status=status.HTTP_200_OK)
                    else:
                          return Response(data=map,status=status.HTTP_400_BAD_REQUEST)
                  else:
                       return Response(status=status.HTTP_400_BAD_REQUEST)
                  
            elif request.method=='DELETE':
                  try:
                   dept=Department.objects.get(Id=pk)
                   time_table=Timetable.objects.get(DepartmentId=dept)
                   try:
                    pub=published.objects.get(DepartmentId=dept) 
                    pub.delete()
                   except:None
                   time_table.delete()
                   return Response(status=status.HTTP_200_OK)
                  except:
                       return Response(status=status.HTTP_400_BAD_REQUEST)

      except Timetable_Lecture.DoesNotExist or Timetable.DoesNotExist:
             return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)   
#manage teacher
@api_view(['POST','GET'])
def teacher(request):
        if request.method=='POST':
                      account_data=json.loads(request.data.get('account'))
                      account=Account()
                      account.Email=account_data['Email']
                      account.Password=account_data['Password']
                      account.save()        
                      role=Role.objects.get(Name='Teacher')
                      account.roles.add(role)
                      account.save()
                      teacher_info=json.loads(request.data.get('teacher'))
                      teacher=Teacher()
                      teacher.Name=teacher_info['Name']
                      teacher.Academic_Degree=teacher_info['Academic_Degree']
                      dep=Department.objects.get(Id=teacher_info['DepartmentId'])
                      teacher.DepartmentId=dep
                      teacher.AccountId=account 
                      teacher.save()
                      const=Constrains()
                      const.TeacherId=teacher
                      const.Sun=True
                      const.Mon=True
                      const.Tue=True
                      const.Wed=True
                      const.Thu=True
                      const.save()
                      return Response(status=status.HTTP_201_CREATED)
                
        elif request.method=='GET':
            teacher=Teacher.objects.all().order_by('Name')
            serializer=Teacher2Serializer(teacher,many=True)
            return Response(serializer.data)
@api_view(['GET'])
def dep_teacher(request,pk):
    try:
      dep=Department.objects.get(Id=pk)
      teacher=Teacher.objects.filter(DepartmentId=dep).order_by('Name')
      if request.method=='GET': 
            serializer=Teacher2Serializer(teacher,many=True)
            return Response(serializer.data)
    except Teacher.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)  
@api_view(['GET'])
def dep_teacher_with_shared(request,pk):
    try: 
      dep=Department.objects.get(Id=pk)
      teacher=Teacher.objects.filter(DepartmentId=dep)
      shared=SharedTeacher.objects.filter(DepartmensId=dep).values("TeacherId")
      
      Steacher=Teacher.objects.filter(id__in=shared) 
      if request.method=='GET': 
            serializer=Teacher2Serializer(teacher|Steacher,many=True)
            return Response(serializer.data) 
    except Teacher.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)  
@api_view(['GET','PUT','DELETE'])  
def teacher_PK(request,pk):
      try:
       teacher=Teacher.objects.get(id=pk)
       if request.method=='GET':    
             serializer=Teacher2Serializer(teacher)
             
             return Response(serializer.data)
       elif request.method=='PUT':
            account=Account.objects.get(id=teacher.AccountId.id)
            Tserializer=TeacherSerializer(teacher,data=json.loads(request.data.get('teacher'))) 
            Account_data=json.loads(request.data.get('account'))
            if Tserializer.is_valid():
               Tserializer.save()
               account.Email=Account_data['Email']
               account.Password=Account_data['Password']
               account.save()
               return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
 
 
       elif request.method=='DELETE':
             account=Account.objects.get(id=teacher.AccountId.id)
             teacher.delete()
             account.delete()
             
             return Response(status=status.HTTP_200_OK)
             
       
      except Teacher.DoesNotExist or Account.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#choose teacher from another department
@api_view(['GET'])
def another_dep_teachers(request,pk):
     if request.method=='GET':
          dept=Department.objects.get(Id=pk)
          teachers=Teacher.objects.exclude(DepartmentId=dept)
          serializer=Teacher2Serializer(teachers,many=True)
          return Response(serializer.data) 
@api_view(['POST'])
def choose_teacher(request):  
      if request.method=='POST': 
            serializer=SharedTeacherSerializer(data=request.data)
            if serializer.is_valid():
                 try:
                       teacher=Teacher.objects.get(id=serializer.validated_data['TeacherId'])
                       shared_teacher=SharedTeacher.objects.get(TeacherId=teacher)
                       dep=Department.objects.get(Id=serializer.validated_data['DepartmensId'])
                       shared_teacher.DepartmensId.append(dep)
                       shared_teacher.save()
                       Teacher_Notify=Teacher_Notification()
                       Teacher_Notify.TeacherId=teacher
                       Teacher_Notify.Content=f"You are choosed as a teacher in {dep.Name} department"
                       Teacher_Notify.date=date.today()
                       Teacher_Notify.seen=False
                       Teacher_Notify.save()
                  
                 except:
                  serializer.save()
                  Teacher_Notify=Teacher_Notification()
                  Teacher_Notify.TeacherId=teacher
                  Teacher_Notify.Content=f"You are choosed as a teacher in {dep.Name} department"
                  Teacher_Notify.date=date.today()
                  Teacher_Notify.seen=False
                  Teacher_Notify.save()
                  return Response(status=status.HTTP_201_CREATED)

            return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)            
@api_view(['GET'])
def shared_teacher(request,pk):
    try:  
      dep=Department.objects.get(Id=pk)
      sharedTeacher=SharedTeacher.objects.filter(DepartmensId__exact=dep).values('TeacherId')
      teacher=Teacher.objects.filter(id__in=sharedTeacher)
      if request.method=='GET':  
            serializer=Teacher2Serializer(teacher,many=True)
            return Response(serializer.data)
    except Teacher.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)  
@api_view(['DELETE'])
def shared_teacher_pk(request,Spk,Dpk):
    try:
      dep=Department.objects.get(Id=Dpk)
      shared_teacher=SharedTeacher.objects.get(TeacherId=Spk)
      if request.method=='DELETE': 
        if shared_teacher.DepartmensId.count()>1:
          shared_teacher.DepartmensId.remove(dep)
          return Response(status=status.HTTP_200_OK)
        else:
          shared_teacher.delete()
          return Response(status=status.HTTP_200_OK)

        
    except Teacher.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)  

#DM notification
@api_view(['GET'])
def DM_notification(request,pk):
       if request.method=='GET':
         try:
            department=Department.objects.get(Id=pk)
            Notification=DM_Notification.objects.filter(DMId=department)
            serializer=DM_NotificationSerializer(Notification,many=True)
            
            return Response(serializer.data)
         except DM_Notification.DoesNotExist :
               return Response(status=status.HTTP_404_NOT_FOUND)

#manage levels
@api_view(['POST','GET'])
def level(request):
        if request.method=='POST':
                serializer=LevelSerializer(data=json.loads(request.data.get('level')))
                if serializer.is_valid():
                      serializer.save()
                      data=serializer.validated_data
                      Groups=data['number_of_groups']
                      print(data['DepartmentId'])
                      level=Level.objects.get(Name=data['Name'],DepartmentId=data['DepartmentId'],number_of_students=data['number_of_students'])
                      if data['Specialization']==True:
                            SpecData=json.loads(request.data.get('Spec'))
                            spec1=Specialization()

                            spec1.Name="network"
                            spec1.LevelId=level
                            spec1.number_of_students=SpecData['network']
                            spec1.save()
                            spec2=Specialization()
                            spec2.Name="programming"
                            spec2.LevelId=level
                            spec2.number_of_students=SpecData['programming']
                            spec2.save()
                      for i in range(Groups):
                            group=Group()
                            group.Name="Group "+str(i+1)
                            group.LevelId=level
                            group.number_of_students=group.LevelId.number_of_students//Groups
                            group.save()
                      return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)            
        elif request.method=='GET':
               level=Level.objects.all()
               serializer=Level2Serializer(level,many=True)
               
               return Response(serializer.data)               
@api_view(['GET'])  
def dep_levels(request,pk):
      try:
       if request.method=='GET':  
             dep=Department.objects.get(Id=pk) 
             level=Level.objects.filter(DepartmentId=dep).order_by('Name')
             list=[]
             
             for lev in level:
              try:     
               net=Specialization.objects.get(LevelId=lev,Name=lev.Name+'network')
               netSerialzer=SpecializationSerializer(net)
              except Specialization.DoesNotExist:
                 netSerialzer=0 
              try:
               prog=Specialization.objects.get(LevelId=lev,Name=lev.Name+'programming')
               progSerialzer=SpecializationSerializer(prog)
              except Specialization.DoesNotExist:
                 progSerialzer=0
              serializer=Level2Serializer(lev)
              list.append({"level":serializer.data,
                   "net":netSerialzer.data if netSerialzer!=0 else 0 ,
                   "prog":progSerialzer.data if progSerialzer!=0 else 0
             })
             return Response(list)
      except Department.DoesNotExist or Level.DoesNotExist or Group.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','PUT','DELETE'])  
def level_PK(request,pk):
      try:
       level=Level.objects.get(id=pk)

       if request.method=='GET':    
             serializer=Level2Serializer(level)
             return Response(serializer.data)
       elif request.method=='PUT':
         serializer=LevelSerializer(level,data=json.loads(request.data.get('level')))
         if serializer.is_valid():
              data=serializer.validated_data
              if (data.get('Specialization')==False and level.Specialization==True):
                        spec=Specialization.objects.filter(LevelId=level)
                        spec.delete()
              if (data.get('Specialization')==True ):
                   NetworkNum=json.loads(request.data.get('Spec'))['network']
                   ProgNum=json.loads(request.data.get('Spec'))['programming']
                   net=Specialization.objects.get(LevelId=level,Name='network')
                   if net.number_of_students!=int(NetworkNum):
                        net.number_of_students=int(NetworkNum)
                        net.save()
                   prog=Specialization.objects.get(LevelId=level,Name='programming')
                   if prog.number_of_students!=int(ProgNum):
                        prog.number_of_students=int(ProgNum)
                        prog.save()
                  
                   level.number_of_students=net.number_of_students+prog.number_of_students
                   level.save
                   if level.Specialization==False:
                            
                            spec1=Specialization()
                            spec1.Name=level.Name+"Network"
                            spec1.LevelId=Level.objects.get(id=level.id)
                            spec1.number_of_students=int(NetworkNum)
                            spec1.save()
                            spec2=Specialization()
                            spec2.Name=level.Name+"programming"
                            spec2.LevelId=Level.objects.get(id=level.id)
                            spec2.number_of_students=int(ProgNum)
                            spec2.save()
              GroupsNum=data.get('number_of_groups')
              groups=Group.objects.filter(LevelId=level).order_by('Name')
              if (GroupsNum!=level.number_of_groups):
                  if GroupsNum>level.number_of_groups:
                    for i in range(GroupsNum-level.number_of_groups):
                            group=Group()
                            group.Name="Group "+str(GroupsNum-level.number_of_groups-i)
                            group.LevelId=level
                            group.number_of_students=level.number_of_students//GroupsNum
                            group.save()
                  elif GroupsNum<level.number_of_groups:
                       for group in range(level.number_of_groups-GroupsNum,0,-1):
                            groups[group-1].delete()
                  for group in groups:
                       group.number_of_students =level.number_of_students//GroupsNum     
                       group.save()    
                            
                            

              serializer.save()
                  
                  
              return Response(status=status.HTTP_200_OK)

       elif request.method=='DELETE':
             level.delete()
             return Response(status=status.HTTP_200_OK)
             
       
      except Level.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#manage groups
@api_view(['GET'])  
def dep_groups(request,pk):
      try:    
       if request.method=='GET':  
             dep=Department.objects.get(Id=pk) 
             level=Level.objects.filter(DepartmentId=dep)
             group=Group.objects.filter(LevelId__in=level).order_by("LevelId",'Name')
             serializer=Group2Serializer(group,many=True)
             return Response(serializer.data)
      except Department.DoesNotExist or Level.DoesNotExist or Group.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)
@api_view(['GET']) 
def level_groups(request,pk):
      try:    
       if request.method=='GET':  
          
             level=Level.objects.get(id=pk)
             group=Group.objects.filter(LevelId=level)
             print(group)
             serializer=Group2Serializer(group,many=True)
             return Response(serializer.data)
      except Department.DoesNotExist or Level.DoesNotExist or Group.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)
@api_view(['GET']) 
def spec_groups(request,pk):
      try:    
       if request.method=='GET':  
             spec=Specialization.objects.get(id=pk)
             group=Group.objects.filter(SpecializationId=spec)
             serializer=Group2Serializer(group,many=True)
             return Response(serializer.data)
      except Department.DoesNotExist or Level.DoesNotExist or Group.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])  
def spec(request,pk):
      try:    
       if request.method=='GET':  
             level=Level.objects.get(id=pk)
             spec=Specialization.objects.filter(LevelId=level)
             serializer=SpecializationSerializer(spec,many=True)
             return Response(serializer.data)
      except Specialization.DoesNotExist or Level.DoesNotExist or Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['PUT'])  
def group_PK(request,pk):
      try:
         if request.method=='PUT':
            group=Group.objects.get(id=pk)
            data=request.data
            old_num=group.number_of_students
            group.Name=data['Name']
            group.LevelId=Level.objects.get(id=data['LevelId'])
            group.number_of_students=data['number_of_students']
            group.SpecializationId=Specialization.objects.get(id=data['SpecializationId'])
            group.save() 
         #شرط عشان يتعدل عدد الطلاب في الدفعة إذاد تعدل حق القروب
            if old_num!=int(request.data.get('number_of_students')):
                        level=Level.objects.get(id=group.LevelId.id)
                        num=0
                        for grop in Group.objects.filter(LevelId=level):
                              num+=grop.number_of_students 
                        level.number_of_students=num
                        level.save()
            return Response(status=status.HTTP_200_OK )
            
      except Group.DoesNotExist or Specialization.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#manage subject
@api_view(['POST'])
def subject(request):
        if request.method=='POST':
                serializer=SubjectSerializer(data=request.data)
                if serializer.is_valid():              
                      serializer.save()
                      return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)                        
@api_view(['GET'])  
def dep_subject(request,pk):    
       if request.method=='GET': 
             #يجلب كل المواد الخاصة بالقسم 
            try:
             department=Department.objects.get(Id=pk)
             subjects=Subject.objects.filter(DepartmentId=department)
              
             serializer=SubjectSerializer(subjects,many=True)
             return Response(serializer.data)
            except Subject.DoesNotExist:
                 return Response(status=status.HTTP_400_BAD_REQUEST)                                
@api_view(['PUT','DELETE'])  
def subject_PK(request,pk):
      try:
       subject=Subject.objects.get(id=pk)
       if request.method=='PUT':
            serializer=SubjectSerializer(subject,data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(status=status.HTTP_200_OK)
       elif request.method=='DELETE':
             subject.delete()
             return Response(status=status.HTTP_200_OK)
      except Subject.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#manage semester subject
@api_view(['POST'])
def semester_subject(request):
        if request.method=='POST':
                try:
                  serializer=SemesterSubjectSerializer(data=request.data)
                except:
                  serializer=SemesterSubjectSerializer(data=request.data,many=True) 
                if serializer.is_valid():
                      data=serializer.validated_data
                      if ((SemesterSubject.objects.filter(SubjectId=data['SubjectId']).count()<2 and Subject.objects.get(id=data['SubjectId'].id).HasLab==True)or(SemesterSubject.objects.filter(SubjectId=data['SubjectId']).count()<1 and Subject.objects.get(id=data['SubjectId'].id).HasLab==False)):
                        serializer.save()
                        subject=Subject.objects.get(id=data['SubjectId'].id)
                        Teacher_Notify=Teacher_Notification()
                        Teacher_Notify.DepartmentId=subject.DepartmentId
                        Teacher_Notify.Content='the semester subject is loaded click to choose'
                        Teacher_Notify.date=datetime.now()
                        Teacher_Notify.seen=False
                        Teacher_Notify.save()
                  
                        return Response(status=status.HTTP_201_CREATED)
                      return Response(serializer.data,status=status.HTTP_208_ALREADY_REPORTED)     
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)     
        elif request.method=='GET': 
             #يجلب كل المواد   
            
             subject=SemesterSubject.objects.all()  
             serializer=SemesterSubject2Serializer(subject,many=True)
             return Response(serializer.data)                   
@api_view(['GET','DELETE'])  
def dep_sem_subject(request,pk):
             #يجلب كل المواد الخاصة بالقسم 
      try:
         department=Department.objects.get(Id=pk)
         subjects=Subject.objects.filter(DepartmentId=department)
         semester_subject=SemesterSubject.objects.filter(SubjectId__in=subjects)  
         if request.method=='GET': 
             map=[]
             for sub in semester_subject:
                  teacher_sub=teacher_subject.objects.filter(Subject=sub).values('teacher')
                  teachers=Teacher.objects.filter(id__in=teacher_sub)
                  Tserializer=Teacher2Serializer(teachers,many=True)
                  Sserializer=SemesterSubject2Serializer(sub)
                  map.append({
                       "subject":Sserializer.data,
                       "teachers":Tserializer.data
                  })
             return Response(map)
         elif request.method=='DELETE':
             semester_subject.delete()
             return Response(status=status.HTTP_200_OK)
      except Department.DoesNotExist:
                 return Response(status=status.HTTP_400_BAD_REQUEST)              
@api_view(['PUT','DELETE'])  
def semestersubject_PK(request,pk):
      try:
       if request.method=='PUT':
            subject=SemesterSubject.objects.get(id=pk)
            serializer=SemesterSubjectSerializer(subject,data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(status=status.HTTP_200_OK)

       elif request.method=='DELETE':
             subject=SemesterSubject.objects.get(id=pk)
             subject.delete()
             return Response(status=status.HTTP_200_OK)
             
       
      except SemesterSubject.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)
@api_view(['POST'])
def teacher_Subject(request):
        if request.method=='POST':
                serializer=TeacherSubjectSerializer(data=request.data)
                if serializer.is_valid():   
                              
                      serializer.save()
                      return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)                        
@api_view(['GET'])  
def dep_teacher_subject(request,pk):
      try:
         if request.method=='GET': 
             department=Department.objects.get(Id=pk)
             subjects=Subject.objects.filter(DepartmentId=department)
             SemSubject=SemesterSubject.objects.filter(SubjectId__in=subjects)
             Tsubject=teacher_subject.objects.filter(Subject__in=SemSubject)
             serializer=TeacherSubject2Serializer(Tsubject,many=True)
             return Response(serializer.data)
         
      except Subject.DoesNotExist:
                 return Response(status=status.HTTP_400_BAD_REQUEST)              
@api_view(['GET'])  
def dep_teacher_of_subject(request,pk):
      try:
         if request.method=='GET': 
             SemSubject=SemesterSubject.objects.filter(id=pk)
             Tsubject=teacher_subject.objects.filter(Subject__in=SemSubject).values('teacher')
             teacher=Teacher.objects.filter(id__in=Tsubject)
             serializer=Teacher2Serializer(teacher,many=True)
             return Response(serializer.data)
         
      except Subject.DoesNotExist:
                 return Response(status=status.HTTP_400_BAD_REQUEST)              
@api_view(['GET']) 
def dep_teacher_subject(request,pk):
      try:
         if request.method=='GET': 
             department=Department.objects.get(Id=pk)
             subjects=Subject.objects.filter(DepartmentId=department)
             SemSubject=SemesterSubject.objects.filter(SubjectId__in=subjects)
             Tsubject=teacher_subject.objects.filter(Subject__in=SemSubject)
             serializer=TeacherSubject2Serializer(Tsubject,many=True)
             return Response(serializer.data)
         
      except Subject.DoesNotExist:
                 return Response(status=status.HTTP_400_BAD_REQUEST)              
@api_view(['GET'])  
def dep_subject_of_teacher(request,pk):
      try:
         if request.method=='GET': 
             teacher=Teacher.objects.filter(id=pk)
             Tsubject=SelectedSubject.objects.filter(Teachers__in=teacher).values('SubjectId')
             semSub=SemesterSubject.objects.filter(id__in=Tsubject).values('SubjectId')
             sub=Subject.objects.filter(id__in=semSub)
             serializer=Subject2Serializer(sub,many=True)
             return Response(serializer.data)
         
      except Teacher.DoesNotExist:
                 return Response(status=status.HTTP_400_BAD_REQUEST)              
@api_view(['GET']) 
def dep_sem_subject_of_teacher(request,pk):
      try:
         if request.method=='GET':
             teachers=Teacher.objects.get(id=pk)
             Tsubject=teacher_subject.objects.filter(teacher=teachers)
             
             serializer=TeacherSubject2Serializer(Tsubject,many=True)
             return Response(serializer.data)
        
      except Teacher.DoesNotExist or Subject.DoesNotExist:
                 return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
def teacher_subject_pk(request,Spk,Tpk):
     try:
      teacher=Teacher.objects.get(id=Tpk)
      subject=SemesterSubject.objects.get(id=Spk)
      TS=teacher_subject.objects.filter(teacher=teacher,Subject=subject)
      if request.method=='DELETE':
             TS.delete()
             return Response(status=status.HTTP_200_OK)
     except teacher_subject.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#manage teachers' selected subject
@api_view(['GET'])  
def dep_selected_subject(request,pk):
      try:
         if request.method=='GET': 
             department=Department.objects.get(Id=pk)
             subjects=Subject.objects.filter(DepartmentId=department)
             SemSubject=SemesterSubject.objects.filter(SubjectId__in=subjects)
             Tsubject=SelectedSubject.objects.filter(SubjectId__in=SemSubject)
             serializer=SelectedSubject2Serializer(Tsubject,many=True)
             return Response(serializer.data)
         
      except Subject.DoesNotExist:
                 return Response(status=status.HTTP_400_BAD_REQUEST)              
 
#manage advertisement
@api_view(['POST'])
def advertisement(request):
        if request.method=='POST':
                serializer=AdvertisementSerializer(data=request.data)
                if serializer.is_valid():   
                      data=serializer.validated_data() 
                      dep=Department.objects.get(Id=data['DepartmentId'])          
                      serializer.save()
                      Student_Notify=Student_Notification()
                      Student_Notify.DepartmentId=dep
                      Student_Notify.Content="new advertisement is published from the department manager"
                      Student_Notify.date=datetime.today()
                      Student_Notify.seen=False
                      Student_Notify.save()
                      teacher_Notify=Teacher_Notification()
                      teacher_Notify.DepartmentId=dep
                      teacher_Notify.Content="new advertisement is published from the department manager"
                      teacher_Notify.date=datetime.today()
                      teacher_Notify.seen=False
                      teacher_Notify.save()
                      return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)                        

#Show Notes
@api_view(['GET'])
def show_teacher_notes(request,pk):
      if request.method=='GET':
            dep=Department.objects.get(Id=pk)
            T_notes=TeacherNote.objects.filter(DepartmentId=dep) 
            T_serializer=TeacherNote2Serializer(T_notes,many=True) 
            return Response(T_serializer.data)
@api_view(['GET'])
def show_student_notes(request,pk):
      if request.method=='GET':
            dep=Department.objects.get(Id=pk)
            S_notes=StudentNote.objects.filter(DepartmentId=dep)
            S_serializer=StudentNote2Serializer(S_notes,many=True)
           
            return Response(S_serializer.data)

#publish timetable
@api_view(['GET'])
def publish(request,pk):
     dep=Department.objects.get(Id=pk) 
     if request.method=='GET':
           try:
             pub=published.objects.get(DepartmentId=dep)
             return Response(status=status.HTTP_400_BAD_REQUEST)
           except:
             pub=published()
             pub.DepartmentId=dep
             pub.save()
             Student_Notify=Student_Notification()
             Student_Notify.DepartmentId=dep
             Student_Notify.Content=" your timetable for this semester is loaded "
             Student_Notify.date=datetime.today()
             Student_Notify.seen=False
             Student_Notify.save()
             teacher_Notify=Teacher_Notification()
             teacher_Notify.DepartmentId=dep
             teacher_Notify.Content=" your timetable for this semester is loaded "
             teacher_Notify.date=datetime.today()
             teacher_Notify.seen=False
             teacher_Notify.save()
             return Response(status=status.HTTP_200_OK)
          
#######################################################Teacher##################################################
#Teacher subject
@api_view(['POST'])
def choose_subject(request):
      if request.method=='POST':
                serializer=SelectedSubjectSerializer(data=request.data,many=True)
                if serializer.is_valid():
                      data=serializer.validated_data
                      serializer.save()
                      semSub=SemesterSubject.objects.get(id=data['SubjectId'])
                      sub=Subject.objects.get(id_=semSub.SubjectId.id)
                      DM_Notufy=DM_Notification()
                      DM_Notufy.DMId=sub.DepartmentId
                      DM_Notufy.Title='subject'
                      DM_Notufy.Content=f"{data['teacher'].Name} chose the subjects"
                      DM_Notufy.date=datetime.now()
                      DM_Notufy.seen=False
                      DM_Notufy.save()
                      return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST) 
@api_view(['DELETE'])
def unchoose_subject(request,pk):
     try:
      subject=SelectedSubject.objects.get(id=pk)
      if request.method=='DELETE':
             subject.delete()
             return Response(status=status.HTTP_200_OK)
     except SelectedSubject.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#Show time table for teacher 

@api_view(['GET'])
def teacher_timetable(request,pk):
      if request.method=='GET':
         try:
           teacher=Teacher.objects.get(id=pk)
           Tlec=[]
           try:
               shared=SharedTeacher.objects.get(TeacherId=teacher).DepartmensId
               pubDept=published.objects.filter(DepartmentId__in=shared).values('DepartmentId')
               lec=Lecture.objects.filter(TeacherId=teacher,DepartmentId__in=pubDept)
               Tlec+=list(Timetable_Lecture.objects.filter(LectureId__in=lec) )
           except:
                None
           
           dept=Department.objects.get(Id=teacher.DepartmentId.Id)
           try:
             pubDept=published.objects.get(DepartmentId=dept)
             lec=Lecture.objects.filter(TeacherId=teacher,DepartmentId=teacher.DepartmentId)
             Tlec+=list(Timetable_Lecture.objects.filter(LectureId__in=lec) )
           except:
                None
           if Tlec!=[]:
            serializer=TLecture2Serializer(Tlec,many=True)
            return Response(serializer.data)
           else:
            return Response(status=status.HTTP_403_FORBIDDEN)
         except Lecture.DoesNotExist or Timetable_Lecture.DoesNotExist:
               return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def teacher_compensation(request,pk):
       if request.method=='GET':
         try:
          teacher=Teacher.objects.get(id=pk)
          lec=Lecture.objects.filter(TeacherId=teacher)
          Tlec=Timetable_Lecture.objects.filter(LectureId__in=lec)
          com=Compensation_Lecture.objects.filter(TimeTableLecId__in=Tlec)
          for i in com:
                  if i.Date==(date.today()-timedelta(days=1)):
                       i.delete()
          serializer=CompensationLecture2Serializer(com,many=True)
          return Response(serializer.data)
         except:
              return Response(status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def teacher_canceled_lecture(request,pk):
       if request.method=='GET':
         try:
          teacher=Teacher.objects.get(id=pk) 
          lec=Lecture.objects.filter(TeacherId=teacher)
          Tlec=Timetable_Lecture.objects.filter(LectureId__in=lec)
          can=Canceled_Lecture.objects.filter(TimeTableLecId__in=Tlec)
          for i in can:
                if i.Date==(date.today()-timedelta(days=1)):
                     i.delete()
          serializer=CanceledLecture2Serializer(can,many=True)
          return Response(serializer.data)
         except:
              return Response(status=status.HTTP_400_BAD_REQUEST)

              
 
@api_view(['GET'])
def teacher_day_timetable(request,pk):
      if request.method=='GET':
         try:
           teacher=Teacher.objects.get(id=pk)
           Tlec=[]
           try:
               shared=SharedTeacher.objects.get(TeacherId=teacher).DepartmensId
               pubDept=published.objects.filter(DepartmentId__in=shared).values('DepartmentId')
               lec=Lecture.objects.filter(TeacherId=teacher,DepartmentId__in=pubDept)
               Tlec+=list(Timetable_Lecture.objects.filter(LectureId__in=lec) )
           except:
                None
           
           dept=Department.objects.get(Id=teacher.DepartmentId.Id)
           try:
             pubDept=published.objects.get(DepartmentId=dept)
             lec=Lecture.objects.filter(TeacherId=teacher,DepartmentId=teacher.DepartmentId)
             Tlec+=list(Timetable_Lecture.objects.filter(LectureId__in=lec,Day=date.today().strftime("%A")) )
           except:
                None
           if Tlec!=[]:
            serializer=TLecture2Serializer(Tlec,many=True)
            return Response(serializer.data)
           else:
            return Response(status=status.HTTP_403_FORBIDDEN)
         except Lecture.DoesNotExist or Timetable_Lecture.DoesNotExist:
               return Response(status=status.HTTP_404_NOT_FOUND)

#teacher notes
@api_view(['POST','GET'])
def teacher_notes(request):
      if request.method=='POST':
            serializer=TeacherNoteSerializer(data=request.data)
            if serializer.is_valid(): 
                  data=serializer.validated_data
                  serializer.save()
                  teacher=Teacher.objects.get(id=data['TeacherId'])
                  DM_Notify=DM_Notification()
                  DM_Notify.DMId=teacher.DepartmentId
                  DM_Notify.Title='teacher_note'
                  DM_Notify.Content=f"{teacher.Name} sent Note click to read"
                  DM_Notify.date=datetime.now()
                  DM_Notify.seen=False
                  DM_Notify.save()
                  return Response(status=status.HTTP_201_CREATED)
            return Response(request.data,status=status.HTTP_400_BAD_REQUEST)           
      elif request.method=='GET':
           note=TeacherNote.objects.all()
           serializer=TeacherNoteSerializer(note,many=True)
           return Response(serializer.data)

#teacher notification
@api_view(['GET'])
def T_notification(request,pk):
       if request.method=='GET':
         try:
            teacher=Teacher.objects.get(id=pk)
            Notification1=list(Teacher_Notification.objects.filter(TeacherId=teacher))
            Notification2=list(Teacher_Notification.objects.filter(DepartmentId=teacher.DepartmentId))
            Notification=Notification1+Notification2
            for i in Notification:
                 i.seen=True
                 i.save()
            serializer=T_NotificationSerializer(Notification,many=True)
            return(serializer.data)
         except Teacher_Notification.DoesNotExist :
               return Response(status=status.HTTP_404_NOT_FOUND)

#Manage constrains
@api_view(['POST','GET'])
def constrains(request):
        if request.method=='POST':
                serializer=ConstrainsSerializer(data=request.data)
                if serializer.is_valid():   
                       data=serializer.validated_data
                       serializer.save()
                       teacher=Teacher.objects.get(id=data['TeacherId'])
                       DM_Notify=DM_Notification()
                       DM_Notify.DMId=teacher.DepartmentId
                       DM_Notify.Title='constrains'
                       DM_Notify.Content=f"{teacher.Name} sent Note click to read"
                       DM_Notify.date=datetime.now()
                       DM_Notify.seen=False
                       DM_Notify.save()    
                      
                       return Response(status=status.HTTP_201_CREATED)
                return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)            
        elif request.method=='GET':
               CR=Constrains.objects.all()
               serializer=Constrains2Serializer(CR,many=True)
            
               return Response(serializer.data)         
@api_view(['GET','PUT','DELETE'])  
def constrains_PK(request,pk):
      try:
       con=Constrains.objects.get(TeacherId=pk)
       if request.method=='GET':    
             serializer=Constrains2Serializer(con)
             return Response(serializer.data)
       elif request.method=='PUT':
            serializer=ConstrainsSerializer(con,data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(status=status.HTTP_200_OK)

       elif request.method=='DELETE':
             con.delete()
             return Response(status=status.HTTP_200_OK)
             
       
      except Constrains.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#cancel lecture
@api_view(['POST'])
def cancel_lecture(request):
      if request.method=='POST':
            serializer=CanceledLectureSerializer(data=request.data)
            if serializer.is_valid():
                  data=serializer.validated_data
                  serializer.save()
                  Tlec=Timetable_Lecture.objects.get(id=data['TimeTableLecId'].id)
                  teacher=Teacher.objects.get(id=Tlec.LectureId.TeacherId.id)
                  DM_Notify=DM_Notification()
                  DM_Notify.DMId=teacher.DepartmentId
                  DM_Notify.Title='cancel_lecture'
                  DM_Notify.Content=f"{teacher.Name} cancel {Tlec.LectureId.SubjectId.SubjectId.Name} lecture for {Tlec.LectureId.LevelId.Name}"
                  DM_Notify.date=datetime.now()
                  DM_Notify.seen=False
                  DM_Notify.save()
                  Student_Notify=Student_Notification()
                  Student_Notify.LevelId=Tlec.LectureId.LevelId
                  Student_Notify.SpeId=Tlec.LectureId.SpecId
                  Student_Notify.GrouplId=Tlec.LectureId.GroupId
                  Student_Notify.Content=f"{teacher.Name} cancel {Tlec.LectureId.SubjectId.SubjectId.Name} lecture "
                  Student_Notify.date=datetime.today()
                  Student_Notify.seen=False
                  Student_Notify.save()

                  return Response(status=status.HTTP_201_CREATED)
            return Response(request.data,status=status.HTTP_400_BAD_REQUEST)           
@api_view(['GET'])  
def canceled_lecture(request,pk):
      try:
       if request.method=='GET':   
             dept=Department.objects.get(Id=pk)
             can=Canceled_Lecture.objects.filter(DepartmentId=dept)
             for i in can:
                  if i.TimeTableLecId.Day==(date.today()-timedelta(days=1)).strftime("%A"):
                       i.delete()
 
             serializer=CanceledLectureSerializer(can,many=True)
             return Response(serializer.data)
       
      except Canceled_Lecture.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])  
def del_canceled_lecture(request,pk):
      try:
       if request.method=='DELETE':
             can=Canceled_Lecture.objects.get(id=pk)
             can.delete()
             return Response(status=status.HTTP_200_OK)
      except Canceled_Lecture.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#request Compensation lecture
@api_view(['POST'])
def Compensation_lecture(request):
      if request.method=='POST':
            serializer=CompensationLectureSerializer(data=request.data)
            if serializer.is_valid(): 
                  data=serializer.validated_data
                  serializer.save()
                  Tlec=Timetable_Lecture.objects.get(id=data['TimeTableLecId'].id)
                  teacher=Teacher.objects.get(id=Tlec.LectureId.TeacherId.id)
                  DM_Notify=DM_Notification() 
                  DM_Notify.DMId=teacher.DepartmentId
                  DM_Notify.Title='compensation_lecture'
                  DM_Notify.Content=f"{teacher.Name} request compensation lecture for {Tlec.LectureId.SubjectId.SubjectId.Name} for {Tlec.LectureId.LevelId.Name}"
                  DM_Notify.date=datetime.now()
                  DM_Notify.seen=False
                  DM_Notify.save()
                  Student_Notify=Student_Notification()
                  Student_Notify.LevelId=Tlec.LectureId.LevelId
                  Student_Notify.SpeId=Tlec.LectureId.SpecId
                  Student_Notify.GrouplId=Tlec.LectureId.GroupId
                  Student_Notify.Content=f"{teacher.Name} request compensation lecture for {Tlec.LectureId.SubjectId.SubjectId.Name} "
                  Student_Notify.date=datetime.today()
                  Student_Notify.seen=False
                  Student_Notify.save()
                  return Response(status=status.HTTP_201_CREATED)
            return Response(request.data,status=status.HTTP_400_BAD_REQUEST)           
@api_view(['GET','PUT','DELETE'])  
def compensation_pk(request,pk):
      try:
       #عشان الحذف والتعديل
       com=Compensation_Lecture.objects.get(id=pk)
       if request.method=='GET':         
             serializer=CompensationLectureSerializer(com)
             return Response(serializer.data)
       elif request.method=='PUT':
            serializer=CompensationLectureSerializer(com,data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(status=status.HTTP_200_OK)

       elif request.method=='DELETE':
             com.delete()
             return Response(status=status.HTTP_200_OK)
      except Compensation_Lecture.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def dep_compensation(request,pk):
       dep=Department.objects.get(Id=pk)
       if request.method=='GET':
          lec=Lecture.objects.filter(DepartmentId=dep)
          Tlec=Timetable_Lecture.objects.filter(LectureId__in=lec)
          com=Compensation_Lecture.objects.filter(TimeTableLecId__in=Tlec)
          for i in com:
                  if i.Date==(date.today()-timedelta(days=1)):
                       i.delete()
          serializer=CompensationLectureSerializer(com,many=True)
          return Response(serializer.data)
 

###################################################student###################################################
#show time table
@api_view(['GET'])
def student_timetable(request,pk):   
      if request.method=='GET':
         try:
            student=Student.objects.get(id=pk) 
            pubDept=published.objects.get(DepartmentId=student.DepartmentId)
            lec1=list(Lecture.objects.filter(LevelId=student.LevelId,GroupId__exact=None,SpecId=None))
            lec2=list(Lecture.objects.filter(LevelId=student.LevelId,GroupId=student.GroupId))
            lec3=list(Lecture.objects.filter(LevelId=student.LevelId,SpecId=student.SpecializationId))
            lec=lec1+lec2+lec3
            Tlec=Timetable_Lecture.objects.filter(LectureId__in=lec) 
            serializer=TLecture2Serializer(Tlec,many=True)
      
            return Response(serializer.data)
         except Lecture.DoesNotExist or Timetable_Lecture.DoesNotExist: 
               return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['GET'])
def student_compensation(request,pk):
       if request.method=='GET':
          student=Student.objects.get(id=pk) 
          lec1=list(Lecture.objects.filter(LevelId=student.LevelId,GroupId__exact=None,SpecId=None))
          lec2=list(Lecture.objects.filter(LevelId=student.LevelId,GroupId=student.GroupId))
          lec3=list(Lecture.objects.filter(LevelId=student.LevelId,SpecId=student.SpecializationId))
          lec=lec1+lec2+lec3
          Tlec=Timetable_Lecture.objects.filter(LectureId__in=lec)
          com=Compensation_Lecture.objects.filter(TimeTableLecId__in=Tlec)
          for i in com:
                  if i.Date==(date.today()-timedelta(days=1)):
                       i.delete()
          serializer=CompensationLecture2Serializer(com,many=True)
          return Response(serializer.data)
@api_view(['GET'])
def student_canceled_lecture(request,pk):
       if request.method=='GET':
          student=Student.objects.get(id=pk) 
          lec1=list(Lecture.objects.filter(LevelId=student.LevelId,GroupId__exact=None,SpecId=None))
          lec2=list(Lecture.objects.filter(LevelId=student.LevelId,GroupId=student.GroupId))
          lec3=list(Lecture.objects.filter(LevelId=student.LevelId,SpecId=student.SpecializationId))
          lec=lec1+lec2+lec3
          Tlec=Timetable_Lecture.objects.filter(LectureId__in=lec)
          com=Canceled_Lecture.objects.filter(TimeTableLecId__in=Tlec)
          for i in com:
                  if i.Date==(date.today()-timedelta(days=1)):
                       i.delete()
          serializer=CanceledLecture2Serializer(com,many=True)
          return Response(serializer.data)

@api_view(['GET'])
def student_timetable_day(request,pk):   
      if request.method=='GET':
         try:
            student=Student.objects.get(id=pk) 
            lec1=list(Lecture.objects.filter(LevelId=student.LevelId,GroupId__exact=None,SpecId=None))
            lec2=list(Lecture.objects.filter(LevelId=student.LevelId,GroupId=student.GroupId))
            lec3=list(Lecture.objects.filter(LevelId=student.LevelId,SpecId=student.SpecializationId))
            lec=lec1+lec2+lec3
            Tlec=Timetable_Lecture.objects.filter(LectureId__in=lec,Day=date.today().strftime("%A")) 
            serializer=TLecture2Serializer(Tlec,many=True)
      
            return Response(serializer.data)
         except Lecture.DoesNotExist or Timetable_Lecture.DoesNotExist: 
               return Response(status=status.HTTP_404_NOT_FOUND)

#student notification
@api_view(['GET'])
def student_notification(request,pk):
      
       student=Student.objects.get(id=pk)
       
       if request.method=='GET':
            Notification1=list(Student_Notification.objects.filter(LevelId=student.LevelId,SpeId=student.SpecializationId,GrouplId=student.GroupId))
            Notification2=list(Student_Notification.objects.filter(LevelId=student.LevelId,SpeId=student.SpecializationId))
            Notification3=list(Student_Notification.objects.filter(LevelId=student.LevelId))
            Notification=Notification1+Notification2+Notification3
            serializer=S_NotificationSerializer(Notification,many=True)
            for i in Notification:
                 i.seen=True
                 i.save()
            return Response(serializer.data)

#student notes
@api_view(["POST"])
def student_note(request):
                  serializer=StudentNoteSerializer(data=request.data)
                  if serializer.is_valid(raise_exception=True):
                    data=serializer.validated_data
                    serializer.save()
                    student=Student.objects.get(id=data['StudentId'])
                    DM_Notify=DM_Notification()
                    DM_Notify.DMId=teacher.DepartmentId
                    DM_Notify.Title='student_note'
                    DM_Notify.Content=f"The student {student.Name} sent Note click to read"
                    DM_Notify.date=datetime.now()
                    DM_Notify.seen=False
                    DM_Notify.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                  else:
                    return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)      
                          
@api_view(['GET'])
def studentNote(request,pk):
	StudentNotes = StudentNote.objects.get(id=pk)
	if StudentNotes:
		serializer = StudentNote2Serializer(StudentNotes, many=False)
		return Response(serializer.data)
	else:
		return Response(status=status.HTTP_404_NOT_FOUND)

     
####################################################shared####################################################
#Login
@api_view(['POST','GET'])
def LogIn(request):
        if request.method=='POST':
                email=request.data.get("Email")
                password=request.data.get('Password')
                try:
                   account=Account.objects.get(Email=email)
                   if account.Password==password:
                       roles=[Role.objects.get(pk=role['id']).Name for role in account.roles.values('id')]
                       dmser=None
                       
                       if 'Teacher' in roles :
                        teacher=Teacher.objects.get(AccountId=account)  
                        dm=DM.objects.filter(TeacherId=teacher)
                        dmser=DM2Serializer(dm,many=True)
                    
                       data={
                            'roles':roles, 
                            'data':info(roles,account),
                            'DM': dmser.data if dmser!=None else None
                           


                            }
                       return Response(data,status=status.HTTP_200_OK)
                   else:
                      return Response(request.data,status=status.HTTP_406_NOT_ACCEPTABLE)
       
                except Account.DoesNotExist:
                     return  Response(request.data,status=status.HTTP_404_NOT_FOUND)
        elif request.method=='GET':
               account=Account.objects.all()
               serializer=AccountSerializer(account,many=True)
               return Response(serializer.data,status=status.HTTP_200_OK)

#empty rooms     
@api_view(['GET'])
def empty_classroom(request,day):
    try:
      
      classroom=Empty_ClassRoom() if day=='0' else Empty_ClassRoom(day.capitalize())
      if request.method=='GET':
            return Response(classroom)
    except Teacher.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

#Adv
@api_view(['GET'])  
def dep_advertisement(request,pk):
      try:
       adv=Advertisement.objects.filter(DepartmentId=pk)
       if request.method=='GET':    
             serializer=AdvertisementSerializer(adv,many=True)
             
             return Response(serializer.data)
      except Advertisement.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

@api_view(['GET','PUT','DELETE'])  
def advertisement_pk(request,pk):
      try:
       adv=Advertisement.objects.get(id=pk)
       if request.method=='PUT':
            serializer=AdvertisementSerializer(adv,data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response(status=status.HTTP_200_OK)
       elif request.method=='DELETE':
            adv.delete()
            return Response(status=status.HTTP_200_OK)

      except Advertisement.DoesNotExist:
            return Response(request.data,status=status.HTTP_404_NOT_FOUND)

@api_view(['post'])
def ChangePassword(request):
      Email=request.data.get('Email')
      Currentpassword=request.data.get('Currentpassword')
      try:
        Accountemail=Account.objects.get(Email=Email)
        if Accountemail.Password==Currentpassword:
                Newpassword=request.data.get('Newpassword')
                Accountemail.Password=Newpassword
                Accountemail.save()
                return Response(status=status.HTTP_200_OK)
        else:
                return Response(request,status=status.HTTP_406_NOT_ACCEPTABLE)
      except Account.DoesNotExist:
                      return Response(request,status=status.HTTP_404_NOT_FOUND)
