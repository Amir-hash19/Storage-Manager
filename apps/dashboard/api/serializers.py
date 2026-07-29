from rest_framework import serializers



class DashboardUsersStatisticsSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    inactive_users = serializers.IntegerField()
    verified_users = serializers.IntegerField()
    unverified_users = serializers.IntegerField()




class TopStorageUserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
    used_storage = serializers.IntegerField()


class DashboardStorageSerializer(serializers.Serializer):
    total_quota = serializers.IntegerField()
    used_storage = serializers.IntegerField()
    free_storage = serializers.IntegerField()
    usage_percent = serializers.FloatField()
    average_usage_per_user = serializers.IntegerField()
    top_users = TopStorageUserSerializer(many=True)