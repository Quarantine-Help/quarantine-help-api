from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from crisis.models import Crisis, Participant
from crisis.serializers import CrisisSerializer, ParticipantSerializer


class CrisisListAPIV1(generics.ListAPIView):
    queryset = Crisis.objects.all()
    serializer_class = CrisisSerializer


class CreateListParticipantsAPIV1(generics.ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
