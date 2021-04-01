from rest_framework import serializers
from .models import Sitecodes_samhsa_ftloc, Siterecs_samhsa_ftloc, Siterecs_samhsa_otp, Siterecs_dbhids_tad, Siterecs_other_srcs, Sites_all

class Sitecodes_samhsa_ftlocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sitecodes_samhsa_ftloc
        fields = '__all__'
class Siterecs_samhsa_ftlocSerializer(serializers.ModelSerializer):
    class Meta:
        model = Siterecs_samhsa_ftloc
        fields = '__all__'


class Siterecs_samhsa_otpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Siterecs_samhsa_otp
        fields = '__all__'

class Siterecs_dbhids_tadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Siterecs_dbhids_tad
        fields = '__all__'

class Siterecs_other_srcsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Siterecs_other_srcs
        fields = '__all__'

class Sites_allSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sites_all
        fields = '__all__'
    