from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    # TODO: задайте требуемые фильтры
    created_at = filters.DateFromToRangeFilter(field_name="created_at")

    class Meta:
        model = Advertisement
        fields = ("status", "creator", "created_at")


# from django_filters import rest_framework as filters
#
# from students.models import Course
#
#
# class CourseFilter(filters.FilterSet):
#
#     id = filters.ModelMultipleChoiceFilter(
#         field_name="id",
#         to_field_name="id",
#         queryset=Course.objects.all(),
#     )
#
#     class Meta:
#         model = Course
#         fields = ("id", "name", )
