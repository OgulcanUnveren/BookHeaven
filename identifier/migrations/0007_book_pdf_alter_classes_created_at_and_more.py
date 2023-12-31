# Generated by Django 4.2.1 on 2023-07-27 13:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identifier', '0006_alter_classes_created_at_alter_school_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pdf',
            field=models.FileField(blank=True, upload_to='books/'),
        ),
        migrations.AlterField(
            model_name='classes',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 27, 13, 27, 11, 303170)),
        ),
        migrations.AlterField(
            model_name='school',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 27, 13, 27, 11, 305421)),
        ),
    ]
