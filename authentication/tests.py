from unittest.mock import patch, MagicMock, Mock

from django.test import TestCase
from django.views import View
from rest_framework import serializers

from authentication.permissions import IsAffectedUser, IsHelperUser, IsOwnerOfRequest
from authentication.serializer import EmailAuthTokenSerializer
from crisis.models import Request


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

participantRequestMock = Mock()
participantRequestMock.owner = Mock()
participantRequestMock.owner.user = currentUser

objectsMock = Mock()
objectsMock.get.return_value = participantRequestMock

SuccessRequestMock = Mock(spec=Request)
SuccessRequestMock.objects = objectsMock

FoundButWrongParticipantRequestMock = Mock()
FoundButWrongParticipantRequestMock.owner = Mock()
# here we return another mock user different from 'owner'
FoundButWrongParticipantRequestMock.user = MockUser()

FoundButWrongObjectsMock = Mock()
FoundButWrongObjectsMock.get.return_value = FoundButWrongParticipantRequestMock

FoundButWrongRequest = Mock(spec=Request)
FoundButWrongRequest.objects = FoundButWrongObjectsMock

# cannot test this because of
# TypeError: catching classes that do not inherit from BaseException is not allowed
# not sure if it is a production issue
# DoesNotExistObjectsMock = Mock()
# DoesNotExistObjectsMock.get.side_effect = ObjectDoesNotExist()
# DoesNotExistRequest = Mock(spec=Request)
# DoesNotExistRequest.objects = DoesNotExistObjectsMock

class IsOwnerOfRequestTest(TestCase):
    def setUp(self) -> None:
        self.model = IsOwnerOfRequest()
        self.viewMock = Mock(spec=View)
        self.viewMock.kwargs = Mock()
        self.viewMock.kwargs.get.return_value = None

    @patch("authentication.permissions.Request", SuccessRequestMock)
    def test_owners_should_have_permission(self):
        request = MockRequest()
        request.user = currentUser

        self.assertTrue(self.model.has_permission(request, self.viewMock))

    @patch("authentication.permissions.Request", FoundButWrongRequest)
    def test_non_owners_should_not_have_permission(self):
        request = MockRequest()
        request.user = currentUser

        self.assertFalse(self.model.has_permission(request, self.viewMock))

    # @patch("authentication.permissions.Request", DoesNotExistRequest)
    # def test_not_found_owner_should_not_have_permission(self):
    #     request = MockRequest()
    #     request.user = currentUser
    #
    #     with self.assertRaises(Http404):
    #         self.assertFalse(self.model.has_permission(request, self.viewMock))
