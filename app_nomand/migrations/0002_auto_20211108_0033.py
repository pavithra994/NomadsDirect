# Generated by Django 3.2.9 on 2021-11-07 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_nomand', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experience',
            name='exptag',
        ),
        migrations.AlterField(
            model_name='hotelinfo',
            name='experiances_tags',
            field=models.ManyToManyField(to='app_nomand.Experience'),
        ),
    ]
