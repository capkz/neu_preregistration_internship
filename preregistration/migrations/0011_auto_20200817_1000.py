# Generated by Django 3.1 on 2020-08-17 07:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('preregistration', '0010_auto_20200814_0846'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='student_status',
            new_name='status',
        ),
        migrations.AlterField(
            model_name='student',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 17, 7, 0, 12, 543612, tzinfo=utc)),
        ),
    ]
