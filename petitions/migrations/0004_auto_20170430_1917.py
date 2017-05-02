from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0003_signature_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='email',
            field=models.CharField(max_length=60),
        ),
    ]
