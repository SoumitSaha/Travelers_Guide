# Generated by Django 2.2.2 on 2019-07-16 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Places', '0013_auto_20190710_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tourist',
            name='password',
        ),
    ]
