import django_filters

from emails.models import Message


class MessageFilter(django_filters.FilterSet):
    is_sent = django_filters.BooleanFilter(
        field_name='sent_at', lookup_expr='isnull', exclude=True
    )
    created_after = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='gte'
    )
    created_before = django_filters.DateTimeFilter(
        field_name='created_at', lookup_expr='lte'
    )

    class Meta:
        model = Message
        fields = ['is_sent', 'created_after', 'created_before']