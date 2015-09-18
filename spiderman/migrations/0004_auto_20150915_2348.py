# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spiderman', '0003_spider_item_model_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpiderRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now=True)),
                ('finish_time', models.DateTimeField(null=True, blank=True)),
                ('finish_reason', models.CharField(max_length=32, choices=[('FL', 'Failed'), ('FN', 'Finished'), ('FSTP', 'Stopped')])),
                ('logfile', models.FileField(upload_to='appdata/logs')),
            ],
            options={
                'ordering': ('start_time',),
            },
        ),
        migrations.RemoveField(
            model_name='spider',
            name='running',
        ),
        migrations.RemoveField(
            model_name='spider',
            name='runtime',
        ),
        migrations.AddField(
            model_name='spiderrun',
            name='spider',
            field=models.ForeignKey(related_name='runs', to='spiderman.Spider'),
        ),
    ]
