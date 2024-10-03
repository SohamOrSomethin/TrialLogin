from django.core.management.base import BaseCommand
import random
from login.models import Student, Subject, StudentSubject


def random_attendance():
    return random.randint(70, 95)

class Command(BaseCommand):
    help = 'Populate StudentSubject table'

    def handle(self, *args, **kwargs):
        students = Student.objects.all()
        subjects = Subject.objects.all()
        
        for student in students:
            for subject in subjects:
                subject_attendance = random_attendance()
                subject_lab_attendance = random_attendance()
            
                StudentSubject.objects.get_or_create(
                    student=student,
                    subject=subject,
                    defaults={
                        'noc_signed': False,
                        'assignments_submitted': False,
                        'subject_attendance': subject_attendance,
                        'subject_lab_attendance': subject_lab_attendance,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated StudentSubject table'))

