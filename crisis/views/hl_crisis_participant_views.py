import datetime

import pytz
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsHelperUser
from crisis.models import Request
from management.serializer import RequestSerializer


class AssignRequestAsHLAPIView(APIView):
    permission_classes = [IsAuthenticated, IsHelperUser]

    def get_object(self, participant_id, request_id):
        try:
            return Request.objects.get(id=request_id, owner=participant_id)
        except Request.DoesNotExist:
            raise Http404("Request not found")

    def post(self, request, *args, **kwargs):
        # Assign the task and see if you can handle it ?
        request_obj = self.get_object(
            participant_id=kwargs.get("participant_id", None),
            request_id=kwargs.get("request_id", None),
        )
        if not request_obj.status == Request.STATUS_PENDING:
            raise Exception("Cannot handle this request, Sorry")

        if not request_obj.deadline > datetime.datetime.utcnow().astimezone(pytz.UTC):
            raise Exception("Too old request, cannot handle. Sorry")

        # Looks good, but lets look a the deadline too ?
        request_obj.assign_user(
            assignee_participant=self.request.user.related_participant
        )
        request_obj.refresh_from_db()
        request_serializer = RequestSerializer(request_obj)
        return Response(request_serializer.data)
