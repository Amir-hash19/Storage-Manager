from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserStorageSerializer, LogOutSerializer, UserProfileSerializer,ChangePasswordSerializer,RegisterLoginResponseSerializer, UserResponseSerializer,LoginSerializer
from apps.accounts.services.retrive_user_storage import RetrieveUserStorageService
from apps.accounts.services.create_user_service import RegisterUserService
from apps.accounts.services.login import LoginUserService
from apps.accounts.services.profile import UserProfileService
from apps.accounts.services.change_password import ChangePasswordService
from apps.accounts.services.logout import AuthService
from apps.accounts.exceptions import UserEmailAlreadyExists, UserNameAlreadyExists, InvalidCredentials, InactiveUser
    

class RegisterView(APIView):
    
    def post(self, request):
        serializer = UserResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = RegisterUserService().execute(
                serializer.validated_data
            )
        except UserEmailAlreadyExists:
            return Response(
                {"detail": "Email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )    
        except UserNameAlreadyExists:
            return Response(
                {"detail":"UserName Already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(
            RegisterLoginResponseSerializer(result).data,
            status=status.HTTP_201_CREATED,
        )
    



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = LoginUserService().execute(
                serializer.validated_data
            )

        except InvalidCredentials:
            return Response(
                {"detail": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )   

        except InactiveUser:
            return Response(
                {"detail":"User Account is inactive."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return Response(
            RegisterLoginResponseSerializer(result).data,
            status=status.HTTP_200_OK
        )
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]


    def post(seld, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ChangePasswordService.execute(
            user=request.user,
            **serializer.validated_data
        )

        return Response(
            {"message":"Password Changed Successfully."},
            status=status.HTTP_200_OK
        )


class RetrieveUserView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user = UserProfileService().get_user_profile(request.user)
        serializer = UserProfileSerializer(user)

        return Response(serializer.data, status=200)






class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogOutSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        AuthService().logout(
            serializer.validated_data["refresh"]
        )
        

        return Response(
            {"detail": "User LogOut Successfully."},
            status=status.HTTP_204_NO_CONTENT
        )




class RetvieveUserStorageView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = UserStorageSerializer

    def get(self, request):
        storage = RetrieveUserStorageService.execute(
                request.user.id
        )

        serializer = self.serializer_class(storage)

        return Response(serializer.data, status=status.HTTP_200_OK)
