from rest_framework import serializers
from apps.storage.models import Folder, File, FileStatus


class CreateFolderSerialzer(serializers.Serializer):
    
    name = serializers.CharField(max_length=255)
    parent_id = serializers.UUIDField(required=False, allow_null=True)




class FolderSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Folder

        fields = [
            "id",
            "name", 
            "path", 
            "parent", 
            "created_at", 
            "updated_at"
        ]




class FolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder

        fields = ["id","name","path","created_at","updated_at"]




class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File

        fields = [
            "id",
            "file_name",
            "size",
            "mime_type",
            "status",
            "created_at"
        ]






class FolderContentsSerializer(serializers.Serializer):
    current_folder = FolderSerializer()
    folders = FolderSerializer(many=True)
    files = FileSerializer(many=True)





class RenameFolderSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=255,
        trim_whitespace=True
    )

    def validateـname(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Folder name can not be empty."
            )

        return value




class FolderListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = (
            "id",
            "name",
            "parent",
            "path",
            "created_at",
            "deleted_at",
        )





class FileUploadSerializer(serializers.Serializer):
    folder_id = serializers.UUIDField()
    file = serializers.FileField()

    def validate_file(self, value):
        if value.size == 0:
            raise serializers.ValidationError("Empty files are not allowed.")

        return value        
    





class FileListSerializer(serializers.ModelSerializer):
    folder_name = serializers.CharField(source="folder.name", read_only=True)

    class Meta:
        model = File
        fields = (
            "id",
            "file_name",
            "extension",
            "mime_type",
            "size",
            "status",
            "folder",
            "folder_name",
            "created_at",
        )




class FileDetailSerializer(serializers.ModelSerializer):
    folder = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = (
            "id",
            "file_name",
            "extension",
            "mime_type",
            "size",
            "checksum",
            "status",
            "folder",
            "created_at",
        )

    def get_folder(self, obj):
        return {
            "id": obj.folder.id,
            "name": obj.folder.name,
        }