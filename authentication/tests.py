from unittest.mock import patch, MagicMock, Mock

from django.test import TestCase
from django.views import View
from rest_framework import serializers

from authentication.permissions import IsAffectedUser, IsHelperUser, IsOwnerOfRequest, IsAssigneeOfRequest
from authentication.serializer import EmailAuthTokenSerializer
from crisis.models.crisis_request import Request


class MockUser:
    def __init__(
            self,
            is_authenticated: bool = False,
    ):
        self.is_authenticated = is_authenticated


class MockRequest:
    pass


class MockRelatedParticipant:
    def __init__(self, type: str = ""):
        self.type = type


failure_authenticate_mock = MagicMock(return_value=None)
success_authenticate_mock = MagicMock(return_value=MockUser())


class EmailAuthTokenSerializerTest(TestCase):
    def setUp(self) -> None:
        self.model = EmailAuthTokenSerializer()

    @patch("authentication.serializer.authenticate", failure_authenticate_mock)
    def test_failed_authentication_should_raise_validation_error(self):
        with self.assertRaisesMessage(serializers.ValidationError, 'Unable to log in with provided credentials.'):
            self.model.validate(attrs=dict(email="test@email.se", password="abc123"))

    def test_missing_credentials_should_throw_exception(self):
        with self.assertRaisesMessage(serializers.ValidationError, 'Must include "email" and "password".'):
            self.model.validate(attrs=dict())

    @patch("authentication.serializer.authenticate", success_authenticate_mock)
    def test_success_authentication_should_return_authenticate_result(self):
        result = self.model.validate(attrs=dict(email="test@email.se", password="abc123"))
        self.assertEquals(type(result['user']), type(MockUser()))


class IsAffectedUserTest(TestCase):
    def setUp(self) -> None:
        self.model = IsAffectedUser()

    def test_request_user_must_be_authenticated_and_affected(self):
        mock_request = MockRequest()
        mock_user = MockUser(is_authenticated=False)
        mock_user.related_participant = MockRelatedParticipant(type="AF")
        mock_request.user = mock_user
        self.assertFalse(self.model.has_permission(mock_request, None))

        mock_request = MockRequest()
        mock_user = MockUser(is_authenticated=True)
        mock_user.related_participant = MockRelatedParticipant(type="SomethingElse")
        mock_request.user = mock_user
        self.assertFalse(self.model.has_permission(mock_request, None))

        mock_request = MockRequest()
        mock_user = MockUser(is_authenticated=False)
        mock_user.related_participant = MockRelatedParticipant(type="SomethingElse")
        mock_request.user = mock_user
        self.assertFalse(self.model.has_permission(mock_request, None))

        mock_request = MockRequest()
        mock_user = MockUser(is_authenticated=True)
        mock_user.related_participant = MockRelatedParticipant(type="AF")
        mock_request.user = mock_user
        self.assertTrue(self.model.has_permission(mock_request, None))


class IsHelperUserTest(TestCase):
    def setUp(self) -> None:
        self.model = IsHelperUser()

    def test_only_helper_can_assign_a_request(self):
        # test that all allowed types have permission as long as authenticated
        allowed_types = ["HL", "AU", "TP"]
        for allowed_type in allowed_types:
            mock_request = MockRequest()
            mock_user = MockUser(is_authenticated=True)
            mock_user.related_participant = MockRelatedParticipant(type=allowed_type)
            mock_request.user = mock_user
            self.assertTrue(self.model.has_permission(mock_request, None))

            mock_request = MockRequest()
            mock_user = MockUser(is_authenticated=False)
            mock_user.related_participant = MockRelatedParticipant(type=allowed_type)
            mock_request.user = mock_user
            self.assertFalse(self.model.has_permission(mock_request, None))

        # test that an authenticated user with an disallowed type does not have permission
        mock_request = MockRequest()
        mock_user = MockUser(is_authenticated=True)
        mock_user.related_participant = MockRelatedParticipant(type="AF")
        mock_request.user = mock_user
        self.assertFalse(self.model.has_permission(mock_request, None))


currentUser = MockUser()

participant_request_mock = Mock()
participant_request_mock.owner = Mock()
participant_request_mock.owner.user = currentUser

objects_mock = Mock()
objects_mock.get.return_value = participant_request_mock

success_request_mock = Mock(spec=Request)
success_request_mock.objects = objects_mock

found_but_wrong_participant_request_mock = Mock()
found_but_wrong_participant_request_mock.owner = Mock()
# here we return another mock user different from 'owner'
found_but_wrong_participant_request_mock.user = MockUser()

found_but_wrong_objects_mock = Mock()
found_but_wrong_objects_mock.get.return_value = found_but_wrong_participant_request_mock

found_but_wrong_request = Mock(spec=Request)
found_but_wrong_request.objects = found_but_wrong_objects_mock


class IsOwnerOfRequestTest(TestCase):
    def setUp(self) -> None:
        self.model = IsOwnerOfRequest()
        self.viewMock = Mock(spec=View)
        self.viewMock.kwargs = Mock()
        self.viewMock.kwargs.get.return_value = None

    @patch("authentication.permissions.Request", success_request_mock)
    def test_owners_should_have_permission(self):
        request = MockRequest()
        request.user = currentUser
        self.assertTrue(self.model.has_permission(request, self.viewMock))

    @patch("authentication.permissions.Request", found_but_wrong_request)
    def test_non_owners_should_not_have_permission(self):
        request = MockRequest()
        request.user = currentUser
        self.assertFalse(self.model.has_permission(request, self.viewMock))


assignee_request = Mock()
assignee_request.assignee = Mock()
assignee_request.assignee.user = currentUser

assignee_objects_mock = Mock()
assignee_objects_mock.get.return_value = assignee_request

assignee_success_request_mock = Mock(spec=Request)
assignee_success_request_mock.objects = assignee_objects_mock


class IsAssigneeOfRequestTest(TestCase):
    def setUp(self) -> None:
        self.model = IsAssigneeOfRequest()
        self.viewMock = Mock(spec=View)
        self.viewMock.kwargs = Mock()
        self.viewMock.kwargs.get.return_value = None

    @patch("authentication.permissions.Request", assignee_success_request_mock)
    def test_owners_should_have_permission(self):
        request = MockRequest()
        request.user = currentUser
        self.assertTrue(self.model.has_permission(request, self.viewMock))
