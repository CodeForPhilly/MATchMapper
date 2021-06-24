from rest_framework import serializers
from .models import Sitecodes_samhsa_ftloc, Siterecs_samhsa_ftloc, Siterecs_samhsa_otp, Siterecs_dbhids_tad, Siterecs_other_srcs, Sites_all, Siterecs_hfp_fqhc

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class Sitecodes_samhsa_ftlocSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Sitecodes_samhsa_ftloc
        fields = '__all__'
class Siterecs_samhsa_ftlocSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Siterecs_samhsa_ftloc
        fields = '__all__'

class Siterecs_hfp_fqhcSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Siterecs_hfp_fqhc
        fields = '__all__'


class Siterecs_samhsa_otpSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Siterecs_samhsa_otp
        fields = '__all__'

class Siterecs_dbhids_tadSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Siterecs_dbhids_tad
        fields = '__all__'

class Siterecs_other_srcsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Siterecs_other_srcs
        fields = '__all__'

class Sites_allSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Sites_all
        fields = '__all__'
    