# Generated by Django 3.1 on 2020-08-30 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterModelTable(
            name='college',
            table='Colleges',
        ),
        migrations.AlterModelTable(
            name='follower',
            table='Follower',
        ),
        migrations.AlterModelTable(
            name='page',
            table='Pages',
        ),
        migrations.AlterModelTable(
            name='profile',
            table='Profiles',
        ),
        migrations.AlterModelTable(
            name='user',
            table='Users',
        ),
    ]
