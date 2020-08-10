from rest_framework import serializers
from .models import Provider

class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['provider_id', 'first_name', 'last_name', 'prefix_name', 'suffix', 'degree','who_id', 'est_rx_cap', 'patient_max', 'date_update']
