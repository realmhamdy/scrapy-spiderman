# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spiderman', '0006_auto_20150916_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='CamoformalcrawlerItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.CharField(max_length=255, null=True, blank=True)),
                ('source_url', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('image', models.ImageField(upload_to=b'spiderfiles/CamoformalSpider/images/%Y/%m/%d/%H/%M/%S')),
                ('sizes', models.CharField(max_length=255, null=True, blank=True)),
                ('spider_run', models.ForeignKey(related_name='webpanel_camoformalcrawleritem_items', to='spiderman.SpiderRun')),
            ],
        ),
        migrations.CreateModel(
            name='SearchdisconnectcrawlerItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=255, null=True, blank=True)),
                ('keyword', models.CharField(max_length=255, null=True, blank=True)),
                ('spider_run', models.ForeignKey(related_name='webpanel_searchdisconnectcrawleritem_items', to='spiderman.SpiderRun')),
            ],
        ),
    ]
