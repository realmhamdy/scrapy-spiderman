# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spiderman', '0007_camoformalcrawleritem_searchdisconnectcrawleritem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='spiderrun',
            options={'ordering': ('-start_time',)},
        ),
        migrations.AlterField(
            model_name='camoformalcrawleritem',
            name='spider_run',
            field=models.ForeignKey(related_name='spiderman_camoformalcrawleritem_items', to='spiderman.SpiderRun'),
        ),
        migrations.AlterField(
            model_name='searchdisconnectcrawleritem',
            name='spider_run',
            field=models.ForeignKey(related_name='spiderman_searchdisconnectcrawleritem_items', to='spiderman.SpiderRun'),
        ),
    ]
