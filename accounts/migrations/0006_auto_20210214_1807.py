# Generated by Django 3.1.3 on 2021-02-14 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210214_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='hash',
            field=models.CharField(default='0x694b92845373c05f3d465f14bb5064cd', max_length=128),
        ),
    ]
