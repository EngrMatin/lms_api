from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]

    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Length must be at least 8 characters")
        
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter")
        
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter")
        
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit")
        
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/~" for char in value):
            raise serializers.ValidationError("Password must contain at least one special character")
        

    def create(self, validated_data):
        user = User(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password)

            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
