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


class RegisterResponseSerializer(serializers.Serializer):
    user = UserResponseSerializer(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)