from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegisterResponseSerializer, UserResponseSerializer

from apps.accounts.services.create_user_service import RegisterUserService

from apps.accounts.exceptions import UserEmailAlreadyExists, UserNameAlreadyExists
    

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
            RegisterResponseSerializer(result).data,
            status=status.HTTP_201_CREATED,
        )