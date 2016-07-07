# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('getpaid', '0002_auto_20150723_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(verbose_name='amount', max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount_paid',
            field=models.DecimalField(default=0, verbose_name='amount paid', max_digits=10, decimal_places=2),
        ),
    ]
