# Generated by Django 3.1.3 on 2021-02-22 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tv', '0008_category_smashup'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategorySmashup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='category',
            name='smashup',
        ),
        migrations.AddConstraint(
            model_name='category',
            constraint=models.UniqueConstraint(fields=('category',), name='unique_category'),
        ),
        migrations.AddField(
            model_name='categorysmashup',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tv.category'),
        ),
        migrations.AddField(
            model_name='categorysmashup',
            name='smashup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tv.smashup'),
        ),
    ]
