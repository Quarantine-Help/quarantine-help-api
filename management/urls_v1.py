from django.urls import path

from authentication.views import CreateParticipantsAPIV1
from management.views import ListCreateRequestsAPIV1

urlpatterns = [
    path("requests/", ListCreateRequestsAPIV1.as_view(), name="create_list_requests")
]
