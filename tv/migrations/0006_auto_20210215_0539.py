# Generated by Django 3.1.3 on 2021-02-15 05:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tv', '0005_auto_20210214_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='smashup',
            name='creator',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='smashup',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='smashup',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='tvimage',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tvimage',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2021, 2, 15, 5, 39, 45, 379872, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tvshow',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='smashup',
            unique_together={('show_1', 'show_2')},
        ),
    ]
