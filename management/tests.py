import json

from django.test import TestCase, Client

from crisis.models.crisis_request import Request


class AssignedRequestsTest(TestCase):
    fixtures = ["fixtures/small.yaml"]
    token = None

    def setUp(self) -> None:
        self.client = Client()

    def testAssignedRequestListEndpointExists(self):
        response = self.client.get("/api/v1/me/assigned-requests/")
        self.assertNotEqual(404, response.status_code)

    def testAssignedRequestListEndpointRequiresAnAuthenticatedUser(self):
        response = self.client.get("/api/v1/me/assigned-requests/")
        self.assertEquals(401, response.status_code)

        response = self.client.get(
            "/api/v1/me/assigned-requests/",
            HTTP_AUTHORIZATION="Token " + self.get_token(),
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(1, response.json()["count"])

    def testAssignedRequestViewEndpointExists(self):
        response = self.client.get("/api/v1/me/assigned-requests/1/")
        self.assertEquals(401, response.status_code)

    def testOnlyAssigneeCanSeeAssignedRequest(self):
        response = self.client.get(
            "/api/v1/me/assigned-requests/2/",
            HTTP_AUTHORIZATION="Token " + self.get_token(),
        )
        self.assertEquals(403, response.status_code)

        response = self.client.get(
            "/api/v1/me/assigned-requests/1/",
            HTTP_AUTHORIZATION="Token " + self.get_token(),
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(response.json()["id"], 1)
        self.assertEquals(response.json()["description"], "toilet paper")

    def testAssigneeCanUpdateRequest(self):
        updated_data = {"status": Request.STATUS_FINISHED}

        response = self.client.patch(
            "/api/v1/me/assigned-requests/1/",
            json.dumps(updated_data),
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + self.get_token(),
        )
        self.assertEquals(200, response.status_code, response.json())

        response = self.client.get(
            "/api/v1/me/assigned-requests/1/",
            HTTP_AUTHORIZATION="Token " + self.get_token(),
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(response.json()["id"], 1)
        self.assertEquals(response.json()["status"], Request.STATUS_FINISHED)

    def testAssigneeCanOnlyUpdateStatus(self):
        # get the item
        response = self.client.get(
            "/api/v1/me/assigned-requests/1/",
            HTTP_AUTHORIZATION="Token " + self.get_token(),
        )
        self.assertEquals(200, response.status_code)

        original_data = response.json()
        updated_data = original_data
        updated_data["description"] = "I really do not want anything"
        updated_data["status"] = "F"

        response = self.client.patch(
            "/api/v1/me/assigned-requests/1/",
            json.dumps(updated_data),
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + self.get_token(),
        )
        self.assertEquals(200, response.status_code, response.json())

        # test setting an invalid status
        response = self.client.patch(
            "/api/v1/me/assigned-requests/1/",
            json.dumps({"status": Request.STATUS_CANCELLED}),
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + self.get_token(),
        )
        self.assertEquals(400, response.status_code, response.json())

        response = self.client.get(
            "/api/v1/me/assigned-requests/1/",
            HTTP_AUTHORIZATION="Token " + self.get_token(),
        )
        self.assertEquals(200, response.status_code)
        self.assertEquals(response.json()["id"], 1)
        self.assertNotEqual(
            response.json()["description"], "I really do not want anything"
        )

    def get_token(self) -> str:
        if self.token is not None:
            return self.token
        response = self.client.post(
            "/api/v1/auth/login/", {"email": "helper1@email.se", "password": "aoeuaoeu"}
        )
        self.token = response.json()["token"]
        return self.token
