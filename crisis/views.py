# Create your views here.
from django.contrib.gis.geos import GEOSGeometry
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from crisis.models import Crisis, Request
from crisis.serializers import CrisisSerializer, AffectedParticipantSerializer
from management.models import Participant
from django.contrib.gis.measure import D


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
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    pass
