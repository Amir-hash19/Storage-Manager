from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from .filters import AuditLogFilter
from core.paginations import DefaultPagination

from apps.dashboard.services.dashboard_service import (
    DashBoardUserStatisticsService,DashBoardStorageService, DashBoardAuditService
)
from apps.dashboard.api.serializers import (
    DashboardUsersStatisticsSerializer,DashboardStorageSerializer, AuditSerializer
)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)

from drf_spectacular.utils import extend_schema



class DashboardUsersView(APIView):

    permission_classes = [IsAdminUser]

    @extend_schema(
            summary="users statistics.",
            description="admin user can see the user statistic like storage usage emaning storage and more...",
            request=DashboardUsersStatisticsSerializer,
            responses={
                202: DashboardUsersStatisticsSerializer
            }
    )

    def get(self, request):
        data = DashBoardUserStatisticsService.execute()

        serializer = DashboardUsersStatisticsSerializer(data)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)




class DashboardStorageView(APIView):
    permission_classes = [IsAdminUser]


    @extend_schema(
            summary="Storage Statistics",
            description="admin user can check the storage statistics.",
            request=DashboardStorageSerializer,
            responses={
                200: DashboardStorageSerializer
            }
    )
    def get(self, request):
        data = DashBoardStorageService.execute()

        serializer = DashboardStorageSerializer(data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    



class DashboardAuditView(ListAPIView):

    serializer_class = AuditSerializer
    permission_classes = [IsAdminUser]

    pagination_class = DefaultPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = AuditLogFilter

    search_fields = (
        "user__username",
        "user__email",
        "action",
        "resource",
        "ip_address",
    )

    ordering_fields = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    def get_queryset(self):
        return DashBoardAuditService.execute()