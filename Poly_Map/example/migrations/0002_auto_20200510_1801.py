# Generated by Django 2.1 on 2020-05-10 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='congress',
            name='contact',
            field=models.CharField(max_length=400),
        ),
    ]
