from django.core.management.base import BaseCommand
from login.models import Student, Subject, StudentSubject

class Command(BaseCommand):
    help = 'Populate StudentSubject table'

    def handle(self, *args, **kwargs):
        students = Student.objects.all()
        subjects = Subject.objects.all()
        
        for student in students:
            for subject in subjects:
                StudentSubject.objects.get_or_create(student=student, subject=subject, noc_signed=False)

        self.stdout.write(self.style.SUCCESS('Successfully populated StudentSubject table'))
