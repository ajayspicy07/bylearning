# Generated by Django 3.1 on 2020-09-06 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0007_auto_20200906_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectbanner',
            name='skills_required',
            field=models.CharField(max_length=2000),
        ),
    ]