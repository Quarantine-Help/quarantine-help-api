from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import IsAssigneeOfRequest
from crisis.models import Request
from management.serializer import RequestSerializer, \
    AssigneeRequestUpdateSerializer


class MeAssignedRequestViewUpdateAPIV1(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAssigneeOfRequest]
    serializer_class = RequestSerializer
    assignee_serializer_class = AssigneeRequestUpdateSerializer
    http_method_names = ["get", "options", "patch", "delete"]

    def get_object(self):
        return Request.objects.get(id=self.kwargs.get("pk", None))

    def destroy(self, request, *args, **kwargs):
        request_object: Request = self.get_object()
        request_object.drop_request_from_assignee()
        # Hack to get a full output.
        self.assignee_serializer_class = self.serializer_class
        return self.retrieve(request=request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        super().update(request=request, *args, **kwargs)
        # Hack to get a full output.
        self.assignee_serializer_class = self.serializer_class
        return self.retrieve(request=request, *args, **kwargs)

    def perform_update(self, serializer):
        """
        An update would be to move something in Transit to Completed. Not
        supporting a move back to assigned sadly at this point.
        :param serializer:
        :return:
        """
        assert serializer.validated_data["status"] == Request.STATUS_FINISHED, (
            "You can only change your status " "to finished on this method."
        )
        self.get_object().resolve_request_from_assignee()
        serializer.save()

    def get_serializer_class(self):
        if self.action in ["partial_update", "destroy"]:
            return self.assignee_serializer_class

        return super().get_serializer_class()


class MeAssignedRequestsAPIV1(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self):
        return (
            Request.objects.filter(assignee__user=self.request.user)
            .exclude(status=Request.STATUS_CANCELLED)
            .order_by("status")
        )
