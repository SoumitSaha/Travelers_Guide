# Generated by Django 2.2.2 on 2019-06-23 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurants', '0002_food'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodAtRestaurants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('sample_pic', models.CharField(max_length=500)),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Restaurants.Food')),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Restaurants.Restaurant')),
            ],
            options={
                'db_table': 'Foods_At_Restaurants',
                'unique_together': {('food_id', 'restaurant_id')},
            },
        ),
    ]
