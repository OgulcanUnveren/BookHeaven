# Generated by Django 4.2.1 on 2023-06-01 17:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0002_auto_20190729_1006"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
