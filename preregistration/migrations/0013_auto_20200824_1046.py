# Generated by Django 3.1 on 2020-08-24 07:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('preregistration', '0012_auto_20200824_0943'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transportation',
            old_name='is_transportation',
            new_name='is_transportation_used',
        ),
        migrations.AlterField(
            model_name='student',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 24, 7, 45, 58, 740533, tzinfo=utc)),
        ),
    ]