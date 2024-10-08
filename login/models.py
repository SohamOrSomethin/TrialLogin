from django.db import models
from django.contrib.auth.models import User

class Division(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)

    def __str__(self):
        return self.name

class Batch(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Subject(models.Model):
    subject_id = models.CharField(max_length=10, unique=True, primary_key=True)
    subject_name = models.CharField(max_length=50)

    def __str__(self):
        return self.subject_name

class StudentSubject(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    assignments_submitted = models.BooleanField(default=False)
    noc_signed = models.BooleanField(default=False)
    subject_attendance = models.IntegerField()
    subject_lab_attendance = models.IntegerField()

    def __str__(self):
        return (f"{self.student} - {self.subject} "
                f"(NOC Signed: {self.noc_signed}) "
                f"(Assignments Submitted: {self.assignments_submitted}) "
                f"subject_attendance: {self.subject_attendance} "
                f"subject_lab_attendance: {self.subject_lab_attendance}")
   
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    registration_number = models.CharField(max_length=20, unique=True, primary_key=True)
    roll_number = models.CharField(max_length=20, unique=True)
    attendance = models.IntegerField(default=0)
    cie_marks = models.IntegerField(default=0)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
   
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    faculty_id = models.CharField(max_length=20, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    subjects = models.ManyToManyField(Subject, blank=True, related_name='faculty')
    batches = models.ManyToManyField(Batch, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"