from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from drf_extra_fields import geo_fields
from rest_framework import serializers, fields
from rest_framework.serializers import ModelSerializer

from authentication.models import User
from management import custom_fields
from management.models import Participant


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserSerializer(ModelSerializer):
    password = fields.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")


class UserSerializerAnonymized(ModelSerializer):
    first_name = custom_fields.AnonymizedStringField()
    last_name = custom_fields.AnonymizedStringField()
    email = custom_fields.AnonymizedEmailField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ParticipantSerializer(ModelSerializer):
    user = UserSerializer()
    position = geo_fields.PointField(str_points=True)

    class Meta:
        model = Participant
        fields = (
            "id",
            "user",
            "position",
            "type",
            "first_line_of_address",
            "second_line_of_address",
            "country",
            "place_id",
            "post_code",
            "city",
            "phone",
            "crisis",
        )


class ParticipantAnonymizedSerializer(ParticipantSerializer):
    user = UserSerializerAnonymized()
    phone = custom_fields.AnonymizedPhoneField()

    class Meta(ParticipantSerializer.Meta):
        pass


class ParticipantsBulkSerializer(serializers.Serializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        fields = ("participants",)
