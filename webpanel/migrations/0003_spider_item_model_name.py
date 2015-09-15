# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webpanel', '0002_auto_20150915_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='spider',
            name='item_model_name',
            field=models.CharField(default='', help_text='Used to refer to the item model for this spider', max_length=128),
            preserve_default=False,
        ),
    ]
