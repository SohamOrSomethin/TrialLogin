# Generated by Django 5.0.7 on 2024-09-11 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_faculty_user_student_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
