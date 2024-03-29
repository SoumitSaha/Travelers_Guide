# Generated by Django 2.2.1 on 2019-07-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Places', '0010_auto_20190709_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='admin',
            name='password',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='email',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='message',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='placereview',
            name='comment',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='verification',
            name='otp',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='verification',
            name='passport_no',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
