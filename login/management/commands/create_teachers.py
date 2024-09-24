import pandas as pd
from django.core.management.base import BaseCommand
from login.models import CustomUser

class Command(BaseCommand):
    help = 'Import teachers from Excel file'

    def handle(self, *args, **kwargs):
        # Example file path (update with your actual file path)
        file_path = r'C:\Users\deole\Desktop\python\NOC\TrialLogin\static\teachers.xlsx'
        df = pd.read_excel(file_path)

        for index, row in df.iterrows():
            CustomUser.objects.create_user(
                username=row['username'],
                password=row['password'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                user_type='teacher'
            )

        self.stdout.write(self.style.SUCCESS('Successfully imported teachers'))
