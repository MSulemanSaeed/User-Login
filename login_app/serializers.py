from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelField):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email', 'phone_number', 'profile_image', 'password', 'confirm_password']