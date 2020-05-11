# Generated by Django 2.1 on 2020-05-10 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0002_auto_20200510_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('progress', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='committee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('importantce', models.IntegerField()),
                ('bills', models.ManyToManyField(to='example.bill')),
                ('members', models.ManyToManyField(to='example.congress')),
            ],
        ),
        migrations.AddField(
            model_name='congress',
            name='bills',
            field=models.ManyToManyField(to='example.bill'),
        ),
    ]
