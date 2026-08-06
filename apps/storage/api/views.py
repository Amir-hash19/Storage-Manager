from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter

from .serializers import( FileListSerializer,FileDetailSerializer, FileUploadSerializer,
RenameFolderSerializer,CreateFolderSerialzer,
FolderSerializer, FolderContentsSerializer, FolderListSerializer )

from .filters import FileFilter


from apps.storage.services.folder_services.rename_folder import RenameFolderService
from apps.storage.services.folder_services.create_folder import FolderCreateService
from apps.storage.services.folder_service import FolderContentService
from apps.storage.services.folder_services.delete_folder import FolderDeleteService
from apps.storage.services.folder_services.restore_folder import FolderRestoreService
from apps.storage.services.folder_services.empty_trash_folder import FolderHardDeleteService
from apps.storage.services.folder_services.list_trash_folder import ListFolderTrashService
from apps.storage.services.download_file import DownloadFileService
from apps.storage.services.file_service import FileService
from apps.storage.services.upload_file import UploadFileService


from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from drf_spectacular.utils import extend_schema

class CreateFolderView(APIView):

    permission_classes = [IsAuthenticated]


    @extend_schema(
        summary="create folder",
        description="Create folder by users.",
    request=CreateFolderSerialzer,
    responses={
            201: FolderSerializer
        }
    )
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

    @extend_schema(
            request=FolderContentsSerializer,
            responses={
                200: FolderContentsSerializer
            }
    )
    def get(self, request, folder_id):

        result = FolderContentService.get_contents(
            owner=request.user,
            folder_id=folder_id
        )
        serializer = FolderContentsSerializer(result)
        
        return Response(serializer.data, status=status.HTTP_200_OK)






class RenameFolderView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="rename folder",
            description="rename folder by users.",
        request=RenameFolderSerializer,
        responses={
            200: FolderSerializer
        }
    )
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

    @extend_schema(
        summary="delete folder",
        description="delete folder by users."
    )
    def delete(self, request, folder_id):
        FolderDeleteService.delete(
            folder_id=folder_id,
            user=request.user
        )

        return Response(
            {"details":"Folder Deleted Successfully."}
            ,status=status.HTTP_204_NO_CONTENT
        )





class FolderRestoreView(APIView):

    permission_classes = [IsAuthenticated]


    @extend_schema(
        summary="restore folder",
        description="restore folder by users."
    )
    def post(self, request, folder_id):

        FolderRestoreService.restore(
            folder_id=folder_id,
            user=request.user
        )

        return Response(
            {"detail":"Folder Restored Successfully."},
            status=status.HTTP_200_OK
        )




class EmptyTrashView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="empty trash",
        description="empty trash by users."
    )
    def delete(self, request):

        result = FolderHardDeleteService.empty_trash(request.user)

        return Response(result, status=status.HTTP_204_NO_CONTENT)
    



class FolderListView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=FolderListSerializer,
        responses={
            200: FolderListSerializer
        },    
        summary="list folders",
        description="list folders by users."
    )
    def get(self, request):

        search = request.query_params.get("search")
        parent = request.query_params.get("parent")
        deleted = (
            request.query_params.get("deleted", "false").lower()
            == "true"
        )

        folders = ListFolderTrashService.search_and_filter(
            user=request.user,
            search=search,
            parent=parent,
            deleted=deleted,
        )

        serializer = FolderListSerializer(
            folders,
            many=True,
        )

        return Response(serializer.data)






class TrashFolderListView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
            summary="list trash folders",
            description="list trash folders by users.",
        request=FolderListSerializer,
        responses={
            200: FolderListSerializer
        }
    )
    def get(self, request):

        folders = ListFolderTrashService.list_trash(
            request.user,
        )

        serializer = FolderListSerializer(
            folders,
            many=True,
        )

        return Response(serializer.data)






class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]


    @extend_schema(
        request=FileUploadSerializer,
        summary="upload file",
        description="upload file by users."
    )

    def post(self, request):

        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        UploadFileService.upload(
            owner=request.user,
            folder_id=serializer.validated_data["folder_id"],
            uploaded_file=serializer.validated_data["file"],
        )

        return Response(
            {
                "detail": "Upload started."
            },
            status=status.HTTP_202_ACCEPTED,
        )




class DownloadfileView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="download file",
        description="download file by users."
    )
    def get(self, request, file_id):
        return DownloadFileService.execute(
            file_id=file_id,
            user=request.user
        )





class FileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
    ):
    
    permission_classes = [IsAuthenticated]

    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    ordering_fields = (
        "created_at",
        "size",
        "file_name",
    )

    ordering = ("-created_at",)

    filterset_class = FileFilter
    
    def get_queryset(self):
        return FileService.get_files(
            owner=self.request.user,
        )
    

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FileDetailSerializer

        return FileListSerializer




class FileDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="delete file",
        description="delete file by users."
    )
    def delete(self, request, file_id):
        FileService.soft_delete(
            owner=request.user,
            file_id=file_id
        )

        return Response(
            {"detail":"Object deleted Successfully."}
            ,status=status.HTTP_204_NO_CONTENT
        )



class FileRestoreView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="restore file",
        description="restore file by users."
    )
    def post(self, request, file_id):

        FileService.restore(
            owner=request.user,
            file_id=file_id
        )

        return Response(status=status.HTTP_200_OK)