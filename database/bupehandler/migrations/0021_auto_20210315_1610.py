# Generated by Django 3.1.7 on 2021-03-15 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bupehandler', '0020_auto_20210310_1546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sites_all',
            name='dbhids_tad_id',
            field=models.ManyToManyField(blank=True, null=True, to='bupehandler.Siterecs_dbhids_tad'),
        ),
        migrations.AlterField(
            model_name='sites_all',
            name='hfp_fqhc_id',
            field=models.ManyToManyField(blank=True, null=True, to='bupehandler.Siterecs_hfp_fqhc'),
        ),
        migrations.AlterField(
            model_name='sites_all',
            name='other_srcs_id',
            field=models.ManyToManyField(blank=True, null=True, to='bupehandler.Siterecs_other_srcs'),
        ),
        migrations.AlterField(
            model_name='sites_all',
            name='samhsa_otp_id',
            field=models.ManyToManyField(blank=True, null=True, to='bupehandler.Siterecs_samhsa_otp'),
        ),
    ]
