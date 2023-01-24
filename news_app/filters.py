from django_filters import FilterSet, CharFilter, DateFilter
from django.forms import DateInput
from .models import Post

class PostFilter(FilterSet):
# виджет для ввода даты
    time_creation = DateFilter(
        lookup_expr='gt',
        widget = DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    class Meta:
        model = Post
        fields = {
            'author': ['exact'],
            'title': ['icontains'],
        }

class SearchFilter(FilterSet):
# фильтр новостей,отображающийся на отдельной странице
    author__identity__username = CharFilter(lookup_expr='icontains')
    title = CharFilter(lookup_expr='icontains')
    time_creation = DateFilter(
        lookup_expr='gt',
        widget = DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    class Meta:
        model = Post
        fields = ('author__identity__username', 'title', 'time_creation')