from django.urls import path
from reports import views


urlpatterns = [
    path("", views.ReportView.as_view(), name="emoticon"),
]
