# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spiderman', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spider',
            name='runtime',
            field=models.DateTimeField(help_text='The last time this spider was started', null=True, blank=True),
        ),
    ]
