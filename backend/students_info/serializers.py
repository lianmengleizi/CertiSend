from rest_framework import serializers
from .models import UserInformation


class UserInformationSerializer(serializers.ModelSerializer):
    full_address = serializers.ReadOnlyField()

    class Meta:
        model = UserInformation
        fields = '__all__'