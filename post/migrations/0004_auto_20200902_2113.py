# Generated by Django 3.1 on 2020-09-02 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20200830_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='postdirectory',
            name='visibility',
            field=models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'My College Only')], default='PRIVATE', max_length=10),
        ),
        migrations.AlterField(
            model_name='postdirectory',
            name='name',
            field=models.CharField(max_length=1000),
        ),
    ]
