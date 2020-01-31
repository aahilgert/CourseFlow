from django.urls import include, path
from . import urls

app_name = "test_course_flow"

urlpatterns = [
    path(
        "", include((urls.urlpatterns, urls.app_name), namespace="course_flow")
    )
]
