from rest_framework import serializers
from apps.storage.models import Folder


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







