# Generated by Django 2.2.1 on 2019-09-13 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Places', '0024_auto_20190913_2013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='aveage_rating',
            new_name='average_rating',
        ),
    ]