from rest_framework.serializers import ModelSerializer

from management.models import Ability


class AbilitySerializer(ModelSerializer):
    class Meta:
        model = Ability
        fields = "__all__"
