from rest_framework import serializers
from apps.accounts.models import UserAccount

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password"
        )


class RegisterLoginResponseSerializer(serializers.Serializer):
    user = UserResponseSerializer(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)