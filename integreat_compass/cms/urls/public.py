from django.urls import path

from ..views import index

urlpatterns = [path("", index.IndexView.as_view(), name="index")]
