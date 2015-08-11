# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signature',
            old_name='last_name',
            new_name='affiliation',
        ),
        migrations.RenameField(
            model_name='signature',
            old_name='first_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='signature',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='signature',
            name='link',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
