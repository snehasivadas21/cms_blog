from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','password']
        read_only_fields = ['id']
        extra_kwargs = {'password':{'write_only':True}}

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken")
        return value

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered")
        return value

    def validate_password(self,value): 
        if len(value)<8:
            raise serializers.ValidationError("At least 8 characters required")
        return value   

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
        