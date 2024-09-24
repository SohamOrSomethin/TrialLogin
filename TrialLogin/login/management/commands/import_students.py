import pandas as pd
from django.core.management.base import BaseCommand
from login.models import CustomUser  

class Command(BaseCommand):
    help = 'Import students from Excel'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\deole\Desktop\python\NOC\TrialLogin\static\FY_IT_B.xlsx'
        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            registration_number = str(row['Registration number'])
            first_name = row['first name']
            last_name = row['last name']
            attendance = row['attendance']
            cie_marks = row['cie marks']

            # Create a new user
            user = CustomUser.objects.create_user(
                username=registration_number,
                password=registration_number,
                first_name=first_name,
                last_name=last_name,
                attendance=attendance,
                cie_marks=cie_marks,
                user_type='student',
            )
            user.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported students'))
