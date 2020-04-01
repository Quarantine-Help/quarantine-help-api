# Create your views here.
import datetime

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.http import Http404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsHelperUser
from crisis.models import Crisis, Request
from crisis.serializers import CrisisSerializer, AffectedParticipantSerializer
from management.models import Participant
from management.serializer import RequestSerializer


class CrisisListAPIV1(generics.ListAPIView):
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer


class ListAffectedParticipantsAPIV1(generics.ListAPIView):
    serializer_class = AffectedParticipantSerializer

    def get_queryset(self):
        crisis_id = self.kwargs.get("crisis_id", None)

        request_type = self.request.query_params.getlist("requestType", [])
        client_latitude = self.request.query_params.get("latitude", None)
        client_longitude = self.request.query_params.get("longitude", None)
        radius = self.request.query_params.get("radius", 7)

        affected_participants = Participant.affected.filter(crisis=crisis_id)

        if request_type:
            affected_participants = affected_participants.filter(
                created_request__type__in=request_type,
                created_request__status__in=Request.UNFINISHED_STATUSES,
            )

        if client_latitude and client_longitude:
            client_longitude = float(client_longitude)
            client_longitude = float(client_longitude)
            geo_point = GEOSGeometry(
                f"POINT({client_longitude} {client_latitude})", srid=4326
            )
            # We need a filtering logic here.
            affected_participants = affected_participants.filter(
                position__distance_lte=(geo_point, D(km=radius))
            )

        return affected_participants


class ListCreateAffectedParticipantRequestsAPIV1(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pass


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

        if not request_obj.deadline > datetime.datetime.utcnow():
            raise Exception("Too old request, cannot handle. Sorry")

        # Looks good, but lets look a the deadline too ?
        request_obj.assign_user(
            assignee_participant=self.request.user.related_participant
        )

        request_obj = request_obj.refresh_from_db()
        request_serializer = RequestSerializer(request_obj)
        return Response(request_serializer.data)
