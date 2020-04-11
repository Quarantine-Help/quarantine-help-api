from django.urls import path

from management.views.af_participant_views import ListCreateRequestsAPIV1, \
    MeRequestDetailAPIV1
from management.views.common_views import MeRetrieveUpdateAPIViewV1
from management.views.hl_participant_views import \
    MeAssignedRequestViewUpdateAPIV1, MeAssignedRequestsAPIV1

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
