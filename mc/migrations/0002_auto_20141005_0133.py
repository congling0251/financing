# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mc', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('term', models.IntegerField()),
                ('part', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('financing_name', models.CharField(max_length=30)),
                ('financing_term', models.IntegerField()),
                ('financing_part', models.IntegerField()),
                ('financing_type', models.CharField(max_length=2)),
                ('from_user', models.CharField(max_length=30)),
                ('to_user', models.CharField(max_length=30)),
                ('amount', models.IntegerField()),
                ('interest', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
