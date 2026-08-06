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


from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from drf_spectacular.utils import extend_schema
    

class RegisterView(APIView):

    @extend_schema(
        summary="User Registration",
        description="""
    Create User Account.

    Response:
        status code 201
        JWT Tokens 
        user account data    

    The frontend does not need to store tokens manually.
    They will be sent automatically with subsequent requests.    
        """,
    request=UserResponseSerializer,
    responses={
            201: RegisterLoginResponseSerializer
        }
    )
    
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

    
    @extend_schema(
        summary="User Login",
        description="""
    Authenticate user using email and password.

    On success:
    - Returns user information.
    - Sets JWT access and refresh tokens in HttpOnly cookies.

    The frontend does not need to store tokens manually.
    They will be sent automatically with subsequent requests.
    """,
        request=LoginSerializer,
        responses={
            200: RegisterLoginResponseSerializer,
            401: OpenApiResponse(
                description="Invalid email or password."
            ),
            403: OpenApiResponse(
                description="User account is inactive."
            ),
        },
        examples=[
            OpenApiExample(
                "Request",
                value={
                    "email": "john@example.com",
                    "password": "StrongPassword123"
                },
                request_only=True,
            )
        ]
    )
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

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(
                description="Password changed successfully."
            ),
            401: OpenApiResponse(
                description="Unauthorized."
            ),
            403: OpenApiResponse(
                description="User account is inactive."
            ),},
        summary="Change Password",
        description="""
    Authenticated users can access this endpoint.
    enter the current password.
    then enter the new password and password confirmation.    

    Response:
        status code 200,
        "message":"Password Changed Successfully."
        
        """
    )
    def post(self, request):
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

    @extend_schema(
        request=UserProfileSerializer,
        summary="Get User Profile",
        description="""
    Authenticated client can access this endpoint.

    retrun:
        user data,
        status code 200    
        """
    )
    def get(self, request):
        user = UserProfileService().get_user_profile(request.user)
        serializer = UserProfileSerializer(user)

        return Response(serializer.data, status=200)






class LogOutView(APIView):
    permission_classes = [IsAuthenticated]


    @extend_schema(
        request=LogOutSerializer,
        summary="logout",
        description="client can log out ."

    )
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

    @extend_schema(
        request=UserStorageSerializer,
        summary="Get user storage usage",
        description="return users storage usage"

    )
    def get(self, request):
        storage = RetrieveUserStorageService.execute(
                request.user.id
        )

        serializer = self.serializer_class(storage)

        return Response(serializer.data, status=status.HTTP_200_OK)
