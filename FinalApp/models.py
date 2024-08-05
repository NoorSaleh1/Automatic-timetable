from django.db import models

# Create your models here.
class Role(models.Model):
    Name=models.CharField(max_length=20)
    def __str__(self):
       return self.Name

class Account(models.Model):
    Email=models.EmailField()
    Password=models.CharField(max_length=50)
    roles = models.ManyToManyField(Role,verbose_name=("roles"))
    def __str__(self):
       return self.Email

class Department(models.Model):
    Id=models.CharField(max_length=10,primary_key=True)
    Name=models.CharField(max_length=15)
    Levels=models.IntegerField()
    period=models.CharField(max_length=5)
    def __str__(self):
       return self.Name

class Teacher(models.Model):
    Name=models.CharField(max_length=50)
    Academic_Degree=models.CharField(max_length=15)
    AccountId=models.ForeignKey(Account,related_name='Account',on_delete=models.SET_NULL,null=True)
    DepartmentId=models.ForeignKey(Department,related_name='Teachers',on_delete=models.CASCADE)
    def __str__(self):
       return self.Name

class SharedTeacher(models.Model):
     TeacherId=models.ForeignKey(Teacher,related_name='SharedTeachers',on_delete=models.CASCADE)
     DepartmensId = models.ManyToManyField(Department,verbose_name=("Departments"))
    
class TeacherNote(models.Model):
        TeacherId=models.ForeignKey(Teacher,related_name='Notes',on_delete=models.CASCADE)
        Title=models.CharField(max_length=30)
        Content=models.CharField(max_length=1000000)
        DepartmentId=models.ForeignKey(Department,related_name='TeacherNotes',on_delete=models.CASCADE)
        def __str__(self):
         return self.Title
 
class Constrains(models.Model):
     TeacherId=models.ForeignKey(Teacher,related_name='Constrains',on_delete=models.CASCADE,null=True)
     Sun=models.BooleanField()
     Mon=models.BooleanField()
     Tue=models.BooleanField()
     Wed=models.BooleanField()
     Thu=models.BooleanField()

class DM(models.Model):
        DepartmentId=models.ForeignKey(Department,related_name='DM',on_delete=models.CASCADE,unique=True)
        TeacherId=models.ForeignKey(Teacher,related_name='DM',on_delete=models.SET_NULL,null=True)
       
class ClassType(models.Model):
         Name=models.CharField(max_length=15)
         def __str__(self):
           return self.Name

class ClassRoom(models.Model):
     Name=models.CharField(max_length=15)
     seating_capacity=models.IntegerField()
     ClassTypeId=models.ForeignKey(ClassType,related_name='ClassRooms',on_delete=models.SET_NULL,null=True)
     def __str__(self):
           return self.Name
     
class Level(models.Model):
     Name=models.CharField(max_length=50)
     DepartmentId=models.ForeignKey(Department,related_name='department',on_delete=models.CASCADE)
     number_of_groups=models.IntegerField()
     number_of_students=models.IntegerField(null=True)
     #only for knowing is she had spec or not
     Specialization=models.BooleanField()
     def __str__(self):
           return self.Name

class Specialization(models.Model):
     Name=models.CharField(max_length=50)
     LevelId=models.ForeignKey(Level,related_name='Specializations',on_delete=models.CASCADE)
     #number_of_groups=models.IntegerField()
     number_of_students=models.IntegerField(null=True)
     def __str__(self):
           return self.Name

class Group(models.Model):
     Name=models.CharField(max_length=50)
     LevelId=models.ForeignKey(Level,related_name='Groups',on_delete=models.CASCADE,null=True)
     SpecializationId=models.ForeignKey(Specialization,related_name='Groups',on_delete=models.CASCADE,null=True)
     number_of_students=models.IntegerField(null=True)
     def __str__(self):
           return self.Name

class Student(models.Model):
     Name=models.CharField(max_length=50)
     LevelId=models.ForeignKey(Level,related_name='Students',on_delete=models.SET_NULL,null=True)
     GroupId=models.ForeignKey(Group,related_name='Students',on_delete=models.SET_NULL,null=True)
     SpecializationId=models.ForeignKey(Specialization,related_name='Studens',on_delete=models.CASCADE,null=True)
     AccountId=models.ForeignKey(Account,related_name='Student',on_delete=models.SET_NULL,null=True)
     DepartmentId=models.ForeignKey(Department,related_name='Students',on_delete=models.CASCADE)
     def __str__(self):
           return self.Name

class StudentNote(models.Model):
        StudentId=models.ForeignKey(Student,related_name='Notes',on_delete=models.CASCADE)
        Title=models.CharField(max_length=30)
        Content=models.CharField(max_length=1000000)
        DepartmentId=models.ForeignKey(Department,related_name='StudentNotes',on_delete=models.CASCADE)

class Subject(models.Model):
    Name=models.CharField(max_length=100)
    DepartmentId=models.ForeignKey(Department,related_name='Subjects',on_delete=models.CASCADE)
    HasLab=models.BooleanField()
    TheoreticalHours=models.IntegerField()
    LabHours=models.IntegerField(null=True)
    Specialization=models.CharField(max_length=50,null=True)
    def __str__(self):
           return self.Name

class SemesterSubject(models.Model):
    SubjectId=models.ForeignKey(Subject,on_delete=models.CASCADE)
    IsLab=models.BooleanField()
    
class teacher_subject(models.Model):
     teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
     Subject=models.ForeignKey(SemesterSubject,on_delete=models.CASCADE)


class SelectedSubject(models.Model):
     SubjectId=models.ForeignKey(SemesterSubject,on_delete=models.CASCADE)
     Teachers=models.ForeignKey(Teacher,on_delete=models.CASCADE)

class Advertisement(models.Model):
     Title=models.CharField(max_length=30)
     Content=models.CharField(max_length=1000000)
     DepartmentId=models.ForeignKey(Department,related_name='Adertisement',on_delete=models.CASCADE,null=True)
     Date=models.DateTimeField(auto_now_add=True)
     def __str__(self):
           return self.Title
     
class Timetable(models.Model):
     DepartmentId=models.ForeignKey(Department,related_name='TimeTable',on_delete=models.CASCADE)

class Lecture(models.Model):
     DepartmentId=models.ForeignKey(Department,related_name='Lectures',on_delete=models.CASCADE)
     LevelId=models.ForeignKey(Level,related_name="Lectures",on_delete=models.CASCADE,null=True)
     GroupId=models.ForeignKey(Group,related_name="Lectures",on_delete=models.CASCADE,null=True)
     SpecId=models.ForeignKey(Specialization,related_name="Lectures",on_delete=models.CASCADE,null=True)
     SubjectId=models.ForeignKey(SemesterSubject,related_name="Lectures",on_delete=models.CASCADE)
     TeacherId=models.ForeignKey(Teacher,related_name="Lectures",on_delete=models.CASCADE)

class Timetable_Lecture(models.Model):
     TimetableId=models.ForeignKey(Timetable,related_name='TLecture',on_delete=models.CASCADE)
     LectureId=models.ForeignKey(Lecture,related_name='TLecture',on_delete=models.CASCADE)
     ClassRoomId=models.ForeignKey(ClassRoom,related_name="TLectures",on_delete=models.SET_NULL,null=True)
     Time=models.CharField(max_length=20)
     Day=models.CharField(max_length=20)

class Canceled_Lecture(models.Model):
     TimeTableLecId=models.ForeignKey(Timetable_Lecture,related_name='CanceledLecture',on_delete=models.CASCADE)
     Reason=models.CharField(max_length=None)
     DepartmentId=models.ForeignKey(Department,related_name='CanceledLecture',on_delete=models.CASCADE)

class Compensation_Lecture(models.Model):
          TimeTableLecId=models.ForeignKey(Timetable_Lecture,related_name='CompensationLecture',on_delete=models.CASCADE)
          Date=models.DateField(null=True)
          NewTime=models.CharField(max_length=20,null=True)
          NewRoomId=models.ForeignKey(ClassRoom,related_name='CompensationLecture',on_delete=models.SET_NULL,null=True)

class Teacher_Notification(models.Model):
     DepartmentId=models.ForeignKey(Department,related_name='DNotification',on_delete=models.CASCADE,null=True)
     TeacherId=models.ForeignKey(Teacher,related_name='Notification',on_delete=models.CASCADE,null=True)
     Content=models.CharField(max_length=1000000)
     date=models.DateTimeField()
     seen=models.BooleanField()

class Student_Notification(models.Model):
     DepartmentId=models.ForeignKey(Department,related_name='SNotification',on_delete=models.CASCADE,null=True)
     LevelId=models.ForeignKey(Level,related_name='Notification',on_delete=models.CASCADE,null=True)
     SpeId=models.ForeignKey(Specialization,related_name='Notification',on_delete=models.CASCADE,null=True)
     GrouplId=models.ForeignKey(Group,related_name='Notification',on_delete=models.CASCADE,null=True)
     Content=models.CharField(max_length=1000000)
     seen=models.BooleanField()
     date=models.DateTimeField()

class DM_Notification(models.Model):
     DMId=models.ForeignKey(Department,related_name='Notification',on_delete=models.CASCADE)
     Title=models.CharField(max_length=1000000)
     Content=models.CharField(max_length=1000000)
     seen=models.BooleanField()    
     date=models.DateTimeField() 

class published(models.Model):
     DepartmentId=models.ForeignKey(Department,related_name='published',on_delete=models.CASCADE)






