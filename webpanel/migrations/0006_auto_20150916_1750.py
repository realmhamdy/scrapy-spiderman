# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpanel', '0005_auto_20150916_1445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spider',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='spiderrun',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
