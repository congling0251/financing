# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mc', '0004_config_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='limit',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
