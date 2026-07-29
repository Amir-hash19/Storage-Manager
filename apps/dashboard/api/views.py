from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status

from apps.dashboard.services.dashboard_service import (
    DashBoardUserStatisticsService,DashBoardStorageService
)
from apps.dashboard.api.serializers import (
    DashboardUsersStatisticsSerializer,DashboardStorageSerializer
)



class DashboardUsersView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        data = DashBoardUserStatisticsService.execute()

        serializer = DashboardUsersStatisticsSerializer(data)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)




class DashboardStorageView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = DashBoardStorageService.execute()

        serializer = DashboardStorageSerializer(data)

        return Response(serializer.data)