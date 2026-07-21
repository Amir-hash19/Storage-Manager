from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import CreateFolderSerialzer, FolderSerializer



from apps.storage.services.create_folder import FolderService




class CreateFolderView(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):

        serializer = CreateFolderSerialzer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        folder = FolderService.create_folder(
            owner=request.user,
            **serializer.validated_data
        )

        return Response(
            FolderSerializer(folder).data,
            status=status.HTTP_201_CREATED
        )
    
