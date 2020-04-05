from django.urls import path

from management.views import (
    ListCreateRequestsAPIV1,
    MeRequestDetailAPIV1,
    MeRetrieveUpdateAPIViewV1,
)

urlpatterns = [
    path("", MeRetrieveUpdateAPIViewV1.as_view(), name="me_retrieve_update"),
    path("requests/", ListCreateRequestsAPIV1.as_view(), name="create_list_requests"),
    path("requests/<int:pk>/", MeRequestDetailAPIV1.as_view(), name="detail_request"),
]
