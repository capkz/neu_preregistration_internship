# Generated by Django 3.1 on 2020-08-24 06:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('preregistration', '0011_auto_20200817_1000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transportation',
            old_name='drop_off_address',
            new_name='dropoff_address',
        ),
        migrations.RenameField(
            model_name='transportation',
            old_name='drop_off_area',
            new_name='dropoff_area',
        ),
        migrations.RenameField(
            model_name='transportation',
            old_name='pick_up_address',
            new_name='pickup_address',
        ),
        migrations.RenameField(
            model_name='transportation',
            old_name='pick_up_area',
            new_name='pickup_area',
        ),
        migrations.RemoveField(
            model_name='disposable_transportation',
            name='name',
        ),
        migrations.RemoveField(
            model_name='disposable_transportation',
            name='pickup_date',
        ),
        migrations.RemoveField(
            model_name='disposable_transportation',
            name='related',
        ),
        migrations.AlterField(
            model_name='parent',
            name='relation',
            field=models.CharField(choices=[('mom', 'Mom'), ('dad', 'Dad')], max_length=8),
        ),
        migrations.AlterField(
            model_name='student',
            name='registration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 24, 6, 43, 55, 173645, tzinfo=utc)),
        ),
    ]