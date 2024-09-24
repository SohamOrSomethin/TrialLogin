import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from login.models import Division, Faculty, Student, Batch, Subject

class Command(BaseCommand):
    help = 'Import students and teachers from Excel'

    def handle(self, *args, **kwargs):
        student_file_path = r'C:\Users\deole\Desktop\python\NOC\TrialLogin\static\students.xlsx'
        teacher_file_path = r'C:\Users\deole\Desktop\python\NOC\TrialLogin\static\teachers.xlsx'
        subject_file_path = r'C:\Users\deole\Desktop\python\NOC\TrialLogin\static\subjects.xlsx'
        batch_file_path = r'C:\Users\deole\Desktop\python\NOC\TrialLogin\static\Batch.xlsx'
        division_file_path = r'C:\Users\deole\Desktop\python\NOC\TrialLogin\static\division.xlsx'
        labs_file_path = r'C:\Users\deole\Desktop\python\NOC\TrialLogin\static\labs.xlsx'

        student_df = pd.read_excel(student_file_path)
        teacher_df = pd.read_excel(teacher_file_path)
        subject_df = pd.read_excel(subject_file_path)
        batch_df = pd.read_excel(batch_file_path)
        division_df = pd.read_excel(division_file_path)
        labs_df = pd.read_excel(labs_file_path)

        # Import Divisions
        for _, row in division_df.iterrows():
            division_name = row['division']
            Division.objects.get_or_create(name=division_name)
        self.stdout.write(self.style.SUCCESS('Successfully imported divisions'))

        # Import Batches
        for _, row in batch_df.iterrows():
            batch_name = row['batch_name']
            division_name = row['division']
            division = Division.objects.get(name=division_name)
            Batch.objects.get_or_create(name=batch_name, division=division)
        self.stdout.write(self.style.SUCCESS('Successfully imported batches'))

        # Import Subjects
        for _, row in subject_df.iterrows():
            subject_id = row['subject_id']
            subject_name = row['subject_name']
            Subject.objects.get_or_create(subject_id=subject_id, subject_name=subject_name)
        self.stdout.write(self.style.SUCCESS('Successfully imported subjects'))

        # Import Students
        for _, row in student_df.iterrows():
            registration_number = str(row['Registration_number'])
            roll_number = row['Roll_Number']
            first_name = row['first_name']
            last_name = row['last_name']
            attendance = row['attendance']
            cie_marks = row['cie_marks']
            batch_name = row['batch']
            division_name = row['division']
            subject_ids = row['subjects'].split(',')

            batch = Batch.objects.get(name=batch_name)
            division = Division.objects.get(name=division_name)

            # Use Django's default User model for password management
            user, created = User.objects.get_or_create(username=registration_number)
            if created:
                user.set_password(registration_number)
                user.save()

            student_user, created = Student.objects.update_or_create(
                registration_number=registration_number,
                defaults={
                    'registration_number': registration_number,
                    'roll_number': roll_number,
                    'first_name': first_name,
                    'last_name': last_name,
                    'attendance': attendance,
                    'cie_marks': cie_marks,
                    'batch': batch,
                    'division': division,
                }
            )
            subjects = Subject.objects.filter(subject_id__in=subject_ids)
            student_user.subjects.set(subjects)
            student_user.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported students'))

        # Import Faculty
        for _, row in teacher_df.iterrows():
            faculty_id = row['faculty_id']
            username = row['username']
            password = row['password']
            first_name = row['first_name']
            last_name = row['last_name']
            email = row['email']
            batch_names = row['batch_name'].split(',')
            subject_ids = row['subject_id'].split(',')

            # Create or get the User
            user, created = User.objects.get_or_create(username=email)
            if created:
                user.set_password(email)
                user.save()

            # Create or update the Faculty
            faculty, created = Faculty.objects.update_or_create(
                faculty_id=faculty_id,
                defaults={
                    'user': user,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                }
            )
            subjects = Subject.objects.filter(subject_id__in=subject_ids)
            faculty.subjects.set(subjects)
            self.stdout.write(self.style.SUCCESS(f"Assigning subjects {subject_ids} to faculty {faculty.faculty_id}"))

            batches = Batch.objects.filter(name__in=batch_names)
            faculty.batches.set(batches)
        