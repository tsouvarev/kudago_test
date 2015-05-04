# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.URLField(max_length=255)),
                ('time_published', models.DateTimeField()),
                ('title', models.TextField()),
                ('summary', models.TextField(default='')),
                ('value', models.TextField()),
            ],
        ),
    ]
