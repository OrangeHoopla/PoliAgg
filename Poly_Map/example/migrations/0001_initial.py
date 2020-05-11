# Generated by Django 2.1 on 2020-05-10 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='congress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=50)),
                ('party', models.CharField(max_length=50)),
                ('district', models.IntegerField()),
                ('state', models.CharField(max_length=50)),
                ('house', models.BooleanField()),
                ('website', models.CharField(max_length=150)),
                ('imageLink', models.CharField(max_length=150)),
                ('congress_num', models.IntegerField()),
            ],
        ),
    ]
