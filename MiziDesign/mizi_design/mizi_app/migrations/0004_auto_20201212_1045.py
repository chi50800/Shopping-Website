# Generated by Django 3.1.4 on 2020-12-12 10:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mizi_app', '0003_auto_20201212_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessrecord',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='accessrecord',
            name='name',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='mizi_app.webpage'),
        ),
        migrations.AddField(
            model_name='webpage',
            name='name',
            field=models.CharField(default='', max_length=264, unique=True),
        ),
        migrations.AddField(
            model_name='webpage',
            name='topic',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='mizi_app.topic'),
        ),
        migrations.AddField(
            model_name='webpage',
            name='url',
            field=models.URLField(default='', unique=True),
        ),
    ]
