from django.urls import path

from authentication.views import EmailAuthToken, CreateParticipantsAPIV1

urlpatterns = [
    path(
        "register/", CreateParticipantsAPIV1.as_view(), name="create_list_participants"
    ),
    path("login/", EmailAuthToken.as_view(), name="login_participant"),
]
