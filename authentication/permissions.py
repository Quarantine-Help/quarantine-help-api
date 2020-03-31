from rest_framework.permissions import BasePermission

import authentication


class IsAffectedUser(BasePermission):
    message = "Only affected participants can create a request"

    def has_permission(self, request, view):
        try:
            return bool(
                request.user.related_participant and request.user.is_authenticated
            )
        except authentication.models.User.related_participant.RelatedObjectDoesNotExist as ex:
            return False
