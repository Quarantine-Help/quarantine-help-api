from django.urls import path

from management.views import (
    ListCreateRequestsAPIV1,
    MeRequestDetailAPIV1,
    MeRetrieveUpdateAPIViewV1,
    MeAssignedRequestsAPIV1,
    MeAssignedRequestViewUpdateAPIV1,
)

urlpatterns = [
    path("", MeRetrieveUpdateAPIViewV1.as_view(), name="me_retrieve_update"),
    path("requests/", ListCreateRequestsAPIV1.as_view(), name="create_list_requests"),
    path("requests/<int:pk>/", MeRequestDetailAPIV1.as_view(), name="detail_request"),
    path("assigned-requests/", MeAssignedRequestsAPIV1.as_view()),
    path(
        "assigned-requests/<int:pk>/",
        MeAssignedRequestViewUpdateAPIV1.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
]
