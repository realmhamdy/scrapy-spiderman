# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webpanel.models.app_models


class Migration(migrations.Migration):

    dependencies = [
        ('webpanel', '0004_auto_20150915_2348'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpiderProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(max_length=255, verbose_name='Path to a spider project found in SPIDER_DIRS setting')),
            ],
            options={
                'ordering': ('path',),
            },
        ),
        migrations.AddField(
            model_name='spiderrun',
            name='stopped',
            field=models.BooleanField(default=False, help_text='Whether the user asked to stop the related spider', editable=False),
        ),
        migrations.AlterField(
            model_name='spiderrun',
            name='finish_reason',
            field=models.CharField(max_length=32, editable=False, choices=[('FL', 'Failed'), ('FN', 'Finished'), ('FUSR', 'Stopped by user')]),
        ),
        migrations.AlterField(
            model_name='spiderrun',
            name='finish_time',
            field=models.DateTimeField(null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='spiderrun',
            name='logfile',
            field=models.FileField(upload_to=webpanel.models.app_models.logfile_uploadto),
        ),
        migrations.AddField(
            model_name='spider',
            name='project',
            field=models.ForeignKey(related_name='spiders', default=None, to='webpanel.SpiderProject'),
            preserve_default=False,
        ),
    ]
