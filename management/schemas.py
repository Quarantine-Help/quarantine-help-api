import coreapi
import coreschema
from rest_framework.schemas import AutoSchema, ManualSchema


class UserSchema(ManualSchema):
    def get_encoding(self, path, method):
        return "application/json"

    def __init__(self):
        manual_fields = [
            coreapi.Field(
                name="email",
                required=True,
                location="body",
                schema=coreschema.String(
                    title="Email", description="Valid email for authentication"
                ),
            ),
            coreapi.Field(
                name="firstName",
                required=True,
                location="body",
                schema=coreschema.String(title="First Name", description="First name"),
            ),
            coreapi.Field(
                name="lastName",
                required=True,
                location="body",
                schema=coreschema.String(title="Last Name", description="Last name"),
            ),
        ]
        super().__init__(fields=manual_fields, encoding="application/json")


class PositionSchema(ManualSchema):
    def __init__(self):
        fields = [
            coreapi.Field(
                "longitude",
                required=True,
                location="body",
                description="Longitude string",
                schema=coreschema.String(),
                example="2.7105760574340807",
            ),
            coreapi.Field(
                "latitude",
                required=True,
                location="body",
                description="Latitude string",
                schema=coreschema.String(),
                example="15.7105760574340807",
            ),
        ]


class ParticipantCreateSchema(ManualSchema):
    def __init__(self):
        manual_fields = [
            coreapi.Field(
                "user",
                required=True,
                location="body",
                description="Participant information",
                schema=coreschema.Ref(UserSchema()),
            ),
            coreapi.Field(
                "position",
                required=True,
                location="body",
                description="Geo Position information",
                schema=coreschema.Ref(PositionSchema()),
                example="{'longitude'': '2.7105760574340807'," "'latitude': '123.3' }",
            ),
            coreapi.Field(
                "type",
                required=True,
                location="formData",
                description="Type of this participant. AF - Affected, " "HL - Helper",
                schema=coreschema.Enum(enum=["HL", "AF", "AU", "TP"], default="AF"),
            ),
            coreapi.Field(
                "firstLineOfAddress",
                required=True,
                location="formData",
                description="First line of address",
                schema=coreschema.String(default="Goerzalle 135"),
            ),
            coreapi.Field(
                "secondLineOfAddress",
                required=True,
                location="formData",
                description="Second line of address",
                schema=coreschema.String(default=""),
            ),
            coreapi.Field(
                "postCode",
                required=True,
                location="formData",
                description="Postcode of the location",
                schema=coreschema.String(default="12207"),
            ),
            coreapi.Field(
                "city",
                required=True,
                location="formData",
                description="City Name",
                schema=coreschema.String(default="Berlin"),
            ),
            coreapi.Field(
                "country",
                required=True,
                location="formData",
                description="Country Code",
                schema=coreschema.String(default="DE"),
            ),
            coreapi.Field(
                "placeId",
                required=True,
                location="formData",
                description="Place Id from Maps App",
                schema=coreschema.String(default="ChIJwyyKo7J3X0YRZ5XOMcLx3xo"),
            ),
            coreapi.Field(
                "crisis",
                required=True,
                location="formData",
                description="Crisis ID we are dealing with",
                schema=coreschema.Number(default=1),
            ),
            coreapi.Field(
                "phone",
                required=False,
                location="formData",
                description="Phone number of the participant",
                schema=coreschema.String(default="+4677777777"),
            ),
        ]
        super().__init__(fields=manual_fields, encoding="application/json")
