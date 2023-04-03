from django_filters import FilterSet, ModelMultipleChoiceFilter, ModelChoiceFilter, CharFilter, DateTimeFilter
from .models import *
from django.forms import DateTimeInput


class PostFilter(FilterSet):
    # author = ModelChoiceFilter(
    #     field_name='post_author',
    #     queryset=Author.objects.all(),
    #     empty_label='любой',
    # )

    post_title = CharFilter(
        field_name='post_title',
        lookup_expr='icontains',
        label='Поиск по названию',
    )

    # post_text = CharFilter(
    #     field_name='post_text',
    #     lookup_expr='icontains',
    # )

    post_category = ModelMultipleChoiceFilter(
        field_name='post_category',
        queryset=Category.objects.all(),
        label='Поиск по категории',
        conjoined=True,
    )

    added_after = DateTimeFilter(
        field_name='post_time_in',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    # class Meta:
    #     model = Post
    #     fields = {'post_text': ['icontains']}
