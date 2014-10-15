# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mc', '0003_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='limit',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
