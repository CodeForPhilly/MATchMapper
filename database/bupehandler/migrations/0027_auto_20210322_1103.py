# Generated by Django 3.1.7 on 2021-03-22 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bupehandler', '0026_siterecs_samhsa_ftloc_tele'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siterecs_dbhids_tad',
            name='loc_suppl',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
