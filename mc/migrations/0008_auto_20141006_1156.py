# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mc', '0007_decision_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='decision',
            name='interest',
            field=models.FloatField(),
        ),
    ]
