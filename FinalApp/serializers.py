from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields='__all__'   

class AccountSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Account
        fields='__all__'  
        read_only_fields = ('id',)

class DepartmentSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Department
        fields='__all__'   

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields='__all__'  
        read_only_fields = ('id',)
class Teacher2Serializer(serializers.ModelSerializer):
    DepartmentId=DepartmentSerializer()
    AccountId=AccountSerializer()
    class Meta:
        model=Teacher
        fields='__all__'  
        read_only_fields = ('id',)

class SharedTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=SharedTeacher
        fields='__all__'  
        read_only_fields = ('id',)
###
class SharedTeacher2Serializer(serializers.ModelSerializer):
    TeacherId=Teacher2Serializer()
    DepartmensId=DepartmentSerializer(many=True)
    class Meta:
        model=SharedTeacher
        fields='__all__'  
        read_only_fields = ('id',)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields='__all__'   

class DMSerializer(serializers.ModelSerializer): 
     class Meta:
        model=DM
        fields='__all__'  
        read_only_fields = ('id',)
class DM2Serializer(serializers.ModelSerializer):
     DepartmentId=DepartmentSerializer()
     TeacherId=TeacherSerializer()
     class Meta:
        model=DM
        fields='__all__'  
        read_only_fields = ('id',)

class ClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ClassType
        fields='__all__'  
        read_only_fields = ('id',)

class ClassRoomSerializer(serializers.ModelSerializer):
      class Meta:
        model=ClassRoom
        fields=['Name','seating_capacity','ClassTypeId']  
        read_only_fields = ('id',)
class ClassRoom2Serializer(serializers.ModelSerializer):
      ClassTypeId =ClassTypeSerializer() 
      class Meta:
        model=ClassRoom
        fields=['id','Name','seating_capacity','ClassTypeId']  
        read_only_fields = ('id',)

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Level
        fields='__all__'  
        read_only_fields = ('id',)
class Level2Serializer(serializers.ModelSerializer):
    DepartmentId=DepartmentSerializer()
    class Meta:
        model=Level
        fields='__all__'  
        read_only_fields = ('id',)

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Specialization
        fields='__all__'  
        read_only_fields = ('id',)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields='__all__'  
        read_only_fields = ('id',)
class Group2Serializer(serializers.ModelSerializer):
    SpecializationId=SpecializationSerializer()
    LevelId=LevelSerializer()
    class Meta:
        model=Group
        fields='__all__'  
        read_only_fields = ('id',)


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'  
        read_only_fields = ('id',)
class Student2Serializer(serializers.ModelSerializer):
    LevelId=LevelSerializer()
    GroupId=GroupSerializer()
    SpecializationId=SpecializationSerializer()
    AccountId=AccountSerializer()
    DepartmentId=DepartmentSerializer()
    class Meta:
        model=Student
        fields='__all__'  
        read_only_fields = ('id',)

class SubjectSerializer(serializers.ModelSerializer):
     class Meta:
        model=Subject
        fields='__all__'  
        read_only_fields = ('id',)
class Subject2Serializer(serializers.ModelSerializer):
     DepartmentId=DepartmentSerializer()
     class Meta:
        model=Subject
        fields='__all__'  
        read_only_fields = ('id',)

class SemesterSubjectSerializer(serializers.ModelSerializer):
     class Meta:
        model=SemesterSubject
        fields='__all__'  
        read_only_fields = ('id',)
class SemesterSubject2Serializer(serializers.ModelSerializer):
     SubjectId=SubjectSerializer()
     class Meta:
        model=SemesterSubject
        fields='__all__'  
        read_only_fields = ('id',)

class TeacherSubjectSerializer(serializers.ModelSerializer):
     class Meta:
        model=teacher_subject
        fields='__all__'  
        read_only_fields = ('id',)
class TeacherSubject2Serializer(serializers.ModelSerializer):
     Subject=SemesterSubject2Serializer()
     teacher=Teacher2Serializer()
     class Meta:
        model=teacher_subject
        fields='__all__'  
        read_only_fields = ('id',)

 
class SelectedSubjectSerializer(serializers.ModelSerializer):
     class Meta:
        model=SelectedSubject
        fields='__all__'  
        read_only_fields = ('id',)
class SelectedSubject2Serializer(serializers.ModelSerializer):
     SubjectId=SemesterSubject2Serializer()
     Teachers=Teacher2Serializer(many=True)
     class Meta:
        model=SelectedSubject
        fields='__all__'  
        read_only_fields = ('id',)

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lecture
        fields='__all__'  
        read_only_fields = ('id',)
class Lecture2Serializer(serializers.ModelSerializer):
    DepartmentId=DepartmentSerializer()
    LevelId=LevelSerializer()
    GroupId=GroupSerializer()
    SpecId=SpecializationSerializer()
    SubjectId=SemesterSubject2Serializer()
    TeacherId=TeacherSerializer()
    class Meta:
        model=Lecture
        fields='__all__'  
        read_only_fields = ('id',)

class TLectureSerializer(serializers.ModelSerializer):
     class Meta:
        model=Timetable_Lecture
        fields='__all__'  
        read_only_fields = ('id',)
    
class TLecture2Serializer(serializers.ModelSerializer):
     LectureId=Lecture2Serializer()
     ClassRoomId=ClassRoom2Serializer()

     class Meta:
        model=Timetable_Lecture
        fields='__all__'  
        read_only_fields = ('id',)

class CanceledLectureSerializer(serializers.ModelSerializer):
    class Meta:
        model=Canceled_Lecture
        fields='__all__'  
        read_only_fields = ('id',)
class CanceledLecture2Serializer(serializers.ModelSerializer):
    TimeTableLecId=TLecture2Serializer()
    DepartmentId=DepartmentSerializer()

    class Meta:
        model=Canceled_Lecture
        fields='__all__'  
        read_only_fields = ('id',) 

class CompensationLectureSerializer(serializers.ModelSerializer):
   
    class Meta:
        model=Compensation_Lecture
        fields='__all__'  
        read_only_fields = ('id',)

class CompensationLecture2Serializer(serializers.ModelSerializer):
    TimeTableLecId=TLecture2Serializer()
    NewRoomId=ClassRoom2Serializer()
    class Meta:
        model=Compensation_Lecture
        fields='__all__'  
        read_only_fields = ('id',)

class TeacherNoteSerializer(serializers.ModelSerializer):
     class Meta:
        model=TeacherNote
        fields='__all__'  
        read_only_fields = ('id',)
class TeacherNote2Serializer(serializers.ModelSerializer):
     TeacherId=Teacher2Serializer()
     DepartmentId=DepartmentSerializer()
     class Meta:
        model=TeacherNote
        fields='__all__'  
        read_only_fields = ('id',)

class T_NotificationSerializer(serializers.ModelSerializer):
     class Meta:
        model=Teacher_Notification
        fields=['Content','date']   

class DM_NotificationSerializer(serializers.ModelSerializer):
     class Meta:
        model=DM_Notification
        fields=['Content','date','seen']   
 
class S_NotificationSerializer(serializers.ModelSerializer):
     class Meta:
        model=Student_Notification
        fields=['Content','date']   

class ConstrainsSerializer(serializers.ModelSerializer):
     class Meta:
        model=Constrains
        fields='__all__'  
        read_only_fields = ('id',)
class Constrains2Serializer(serializers.ModelSerializer):
     TeacherId=Teacher2Serializer()
     class Meta:
        model=Constrains
        fields='__all__'  
        read_only_fields = ('id',)

class AdvertisementSerializer(serializers.ModelSerializer):
     class Meta:
        model=Advertisement
        fields='__all__'  
        read_only_fields = ('id',)

class StudentNoteSerializer(serializers.ModelSerializer):
     class Meta:
        model=StudentNote
        fields='__all__'  
        read_only_fields = ('id',)
class StudentNote2Serializer(serializers.ModelSerializer):
     StudentId=Student2Serializer()
     class Meta:
        model=StudentNote
        fields='__all__'  
        read_only_fields = ('id',)