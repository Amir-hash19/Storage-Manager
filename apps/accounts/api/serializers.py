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



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password":"Password do not match."}
            )
        return attrs



class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAccount
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "avatar",
            "storage_quota",
            "used_storage",
            "is_verified"

        )





class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()





class UserStorageSerializer(serializers.ModelSerializer):

    storage_quota_gb = serializers.SerializerMethodField()
    used_storage_mb = serializers.SerializerMethodField()

    class Meta:
        model = UserAccount
        fields = (
            "storage_quota",
            "used_storage",
            "storage_quota_gb",
            "used_storage_mb",
        )

    def get_storage_quota_gb(self, obj):
        return round(obj.storage_quota / (1024 ** 3), 2)

    def get_used_storage_mb(self, obj):
        return round(obj.used_storage / (1024 ** 2), 2)