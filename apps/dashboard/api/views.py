from django.db import connection
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (OpenApiExample, OpenApiResponse,
                                   extend_schema)
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.dashboard.api.serializers import (AuditSerializer,
                                            DashboardStorageSerializer,
                                            DashboardUsersStatisticsSerializer)
from apps.dashboard.services.dashboard_service import (
    DashBoardAuditService, DashBoardStorageService,
    DashBoardUserStatisticsService)
from core.paginations import DefaultPagination

from .filters import AuditLogFilter


class DashboardUsersView(APIView):

    permission_classes = [IsAdminUser]

    @extend_schema(
        summary="users statistics.",
        description="admin user can see the user statistic like storage usage emaning storage and more...",
        request=DashboardUsersStatisticsSerializer,
        responses={202: DashboardUsersStatisticsSerializer},
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
        responses={200: DashboardStorageSerializer},
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

    ordering_fields = ("created_at",)

    ordering = ("-created_at",)

    def get_queryset(self):
        return DashBoardAuditService.execute()


# liveness Prob


def liveness(request):
    return JsonResponse({"status": "OK"})


# readiness Prob
def readiness(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return JsonResponse({"status": "Ready!"})
    except Exception:
        return JsonResponse({"status": "not ready"}, status=503)
