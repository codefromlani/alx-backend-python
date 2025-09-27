import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.NumberFilter(field_name="sender__id")
    recipient = django_filters.NumberFilter(field_name="recipient__id")
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'recipient', 'start_date', 'end_date']
