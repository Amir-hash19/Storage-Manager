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





class ForgetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()    




class ResetPasswordSerializer(serializers.Serializer):

    token = serializers.CharField()

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
    )