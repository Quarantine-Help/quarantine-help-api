from django.http import Http404
from rest_framework.permissions import BasePermission

import authentication
from crisis.models import Request


class IsAffectedUser(BasePermission):
    message = "Only affected participants work on requests"

    def has_permission(self, request, view):
        try:
            return bool(
                request.user.related_participant.type == "AF"
                and request.user.is_authenticated
            )
        except authentication.models.User.related_participant.RelatedObjectDoesNotExist as ex:
            return False


class IsHelperUser(BasePermission):
    message = "Only helpers can assign a request"

    def has_permission(self, request, view):
        try:
            return bool(
                request.user.related_participant.type in ["HL", "AU", "TP"]
                and request.user.is_authenticated
            )
        except authentication.models.User.related_participant.RelatedObjectDoesNotExist as ex:
            return False


class IsOwnerOfRequest(BasePermission):
    message = "You do not have the permission to manage this request"

    def has_permission(self, request, view):
        try:
            participant_request = Request.objects.get(id=view.kwargs.get("pk", None))
        except Request.DoesNotExist:
            raise Http404("Not found")
        return participant_request.owner.user == request.user
