# Create your views here.
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema

from authentication.models import User
from authentication.schemas import ParticipantCreateSchema
from authentication.serializer import EmailAuthTokenSerializer, ParticipantSerializer
from crisis.helpers import generate_username_with_user_data


class EmailAuthToken(ObtainAuthToken):
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location="body",
                    schema=coreschema.String(
                        title="Email", description="Valid email for authentication"
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location="form",
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "participantId": user.related_participant.id,
                "email": user.email,
            }
        )


class CreateParticipantsAPIV1(generics.CreateAPIView):
    serializer_class = ParticipantSerializer
    schema = ParticipantCreateSchema()

    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        user_data = validated_data["user"]

        username = generate_username_with_user_data(user_data=user_data)

        user_data["username"] = username
        user = User.objects.create(**validated_data["user"])
        if not user_data.get("password", None):
            user.set_unusable_password()
            # Also send out an email ?
        else:
            user.set_password(user_data["password"])

        user.save()
        user.refresh_from_db()
        serializer.save(user=user)
        return
