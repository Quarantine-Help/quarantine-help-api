from rest_framework import fields, serializers
from rest_framework.serializers import ModelSerializer

from authentication.serializer import UserSerializer, ParticipantSerializer
from crisis.models.crisis_request import Request
from crisis.models.request_assignment import RequestAssignment
from management.models import Ability


class AbilitySerializer(ModelSerializer):
    class Meta:
        model = Ability
        fields = "__all__"


class RequestAssignmentSerializer(ModelSerializer):
    class Meta:
        model = RequestAssignment
        fields = ("status", "id", "created_at", "did_complete", "assignee_id")


class RequestSerializer(ModelSerializer):
    assignee = ParticipantSerializer(allow_null=True, required=False, read_only=True)
    assignmentHistory = RequestAssignmentSerializer(
        source="related_assignment",
        allow_null=True,
        required=False,
        read_only=True,
        many=True,
    )
    status = fields.CharField(required=False, allow_null=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        # We do not allow people to set attribute to Transit through the API
        # view. al
        if not self.instance:
            return attrs

        if self.instance.status in Request.FINISHED_STATUSES:
            raise serializers.ValidationError("You cannot change this request anymore.")

        if self.instance.status == "T":
            if attrs["status"] not in Request.FINISHED_STATUSES:
                raise serializers.ValidationError(
                    "You can only cancel or mark the request as finished"
                )
            if attrs["description"] != self.instance.description:
                raise serializers.ValidationError(
                    "You will have to cancel this request first."
                )
            if not attrs["deadline"] >= self.instance.deadline:
                raise serializers.ValidationError(
                    "You cannot shorten the deadline now. Please cancel"
                )

        if attrs["status"] == "T":
            raise serializers.ValidationError("Cannot update the status to T")
        return attrs

    class Meta:
        model = Request
        fields = (
            "id",
            "type",
            "deadline",
            "description",
            "assignee",
            "status",
            "assignmentHistory",
            "created_at",
        )


class AssigneeRequestUpdateSerializer(ModelSerializer):
    class Meta:
        model = Request
        fields = ("id", "status")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if "status" not in attrs:
            raise serializers.ValidationError("Status is mandatory")

        allowed_status = [Request.STATUS_FINISHED, Request.STATUS_TRANSIT]
        if attrs["status"] not in allowed_status:
            raise serializers.ValidationError(
                "Only the following status are allowed %s" % str(allowed_status)
            )

        return attrs
