# Generated by Django 5.0.7 on 2024-09-02 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_customuser_batch'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='roll_no',
            field=models.IntegerField(default=0),
        ),
    ]
