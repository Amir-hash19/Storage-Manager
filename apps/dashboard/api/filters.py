import django_filters
from apps.audit.models import AuditLog




class AuditLogFilter(django_filters.FilterSet):

    from_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte",
    )

    to_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte",
    )

    class Meta:
        model = AuditLog
        fields = [
            "action",
            "resource",
            "status",
            "user",
        ]