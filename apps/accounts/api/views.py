from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterLoginResponseSerializer, UserResponseSerializer,LoginSerializer

from apps.accounts.services.create_user_service import RegisterUserService
from apps.accounts.services.login import LoginUserService

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