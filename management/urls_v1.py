from django.urls import path

from management.views import CreateParticipantsAPIV1

urlpatterns = [
    path("", CreateParticipantsAPIV1.as_view(), name="create_list_participants")
]
