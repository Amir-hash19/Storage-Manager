from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .serializers import RenameFolderSerializer,CreateFolderSerialzer, FolderSerializer, FolderContentsSerializer


from apps.storage.services.rename_folder import RenameFolderService
from apps.storage.services.create_folder import FolderCreateService
from apps.storage.services.folder_service import FolderContentService
from apps.storage.services.delete_folder import FolderDeleteService



class CreateFolderView(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request):

        serializer = CreateFolderSerialzer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        folder = FolderCreateService.create_folder(
            owner=request.user,
            **serializer.validated_data
        )

        return Response(
            FolderSerializer(folder).data,
            status=status.HTTP_201_CREATED
        )
    


class FolderContentsView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request, folder_id):

        result = FolderContentService.get_contents(
            owner=request.user,
            folder_id=folder_id
        )
        serializer = FolderContentsSerializer(result)
        
        return Response(serializer.data, status=status.HTTP_200_OK)






class RenameFolderView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, folder_id):
        serializer = RenameFolderSerializer(
            data=request.data
        )    

        serializer.is_valid(raise_exception=True)

        folder = RenameFolderService.execute(
            folder_id=folder_id,
            owner=request.user,
            new_name=serializer.validated_data["name"]
        )

        return Response(
            {
                "details":"Folder Renamed Successfully.",
                "data":{
                    "id": folder.id,
                    "name": folder.name,
                    "path": folder.path,
                },
            },
            status=status.HTTP_200_OK,
        )





class FolderDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, folder_id):
        FolderDeleteService.delete(
            folder_id=folder_id,
            user=request.user
        )

        return Response(
            {"details":"Folder Deleted Successfully."}
            ,status=status.HTTP_204_NO_CONTENT
        )