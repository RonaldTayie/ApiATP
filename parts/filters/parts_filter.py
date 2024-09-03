# filters.py
import django_filters
from parts.models import Part, Category


class PartFilter(django_filters.FilterSet):
    # Filter by part name
    part = django_filters.CharFilter(lookup_expr='icontains', label='Part Name')
    # Filter by category name and include nested categories
    category = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains',
        label='Category Name'
    )
    # Custom filter to handle nested categories
    category_path = django_filters.CharFilter(method='filter_by_category_path', label='Category Path')
    class Meta:
        model = Part
        fields = ['part', 'part_description', 'category', 'category_path']

    def filter_by_category_path(self, queryset, name, value):
        """
        Custom filter to match parts where the category is in the specified category path.
        """
        # Split the category path by ' > ' to get individual category names
        category_names = value.split(' > ')

        # Find all categories in the path
        categories = Category.objects.filter(name__in=category_names)

        # Use a subquery to filter parts based on whether their category is in the path
        if categories.exists():
            category_ids = categories.values_list('id', flat=True)
            queryset = queryset.filter(category__in=category_ids)

        return queryset
