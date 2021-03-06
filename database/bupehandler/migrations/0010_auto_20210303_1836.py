# Generated by Django 3.1.7 on 2021-03-03 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bupehandler', '0009_auto_20210303_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='siterecs_samhsa_otp',
            name='data_review',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='siterecs_samhsa_otp',
            name='date_full_certification',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='siterecs_samhsa_otp',
            name='name_dba',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='siterecs_samhsa_otp',
            name='name_program',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='siterecs_samhsa_otp',
            name='zipcode',
            field=models.CharField(max_length=10),
        ),
    ]
