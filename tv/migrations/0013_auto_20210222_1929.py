# Generated by Django 3.1.3 on 2021-02-22 19:29

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tv', '0012_auto_20210222_1918'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='categoryscore',
            name='unique_category_score_user',
        ),
        migrations.AlterUniqueTogether(
            name='categoryscore',
            unique_together={('user', 'categorysmashup')},
        ),
    ]
