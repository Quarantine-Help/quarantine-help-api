from datetime import datetime

from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from rest_framework import generics

from crisis.models.crisis import Crisis
from crisis.models.crisis_request import Request
from crisis.serializers import AffectedParticipantSerializer, CrisisSerializer
from management.models import Participant


class ListAffectedParticipantsAPIV1(generics.ListAPIView):
    serializer_class = AffectedParticipantSerializer

    def get_queryset(self):
        crisis_id = self.kwargs.get("crisis_id", None)

        request_type = self.request.query_params.getlist("requestType", [])
        client_latitude = self.request.query_params.get("latitude", None)
        client_longitude = self.request.query_params.get("longitude", None)
        radius = self.request.query_params.get("radius", 7)

        affected_participants = Participant.affected.filter(
            crisis=crisis_id,
            created_request__deadline__gte=datetime.utcnow()
        )

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


class CrisisListAPIV1(generics.ListAPIView):
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer