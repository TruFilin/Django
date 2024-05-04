import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='Start Date')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='End Date')

    class Meta:
        model = Post
        fields = ['created_at']

