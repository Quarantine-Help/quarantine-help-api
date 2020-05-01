from rest_framework import serializers, fields


class CountrySerializerV1(serializers.Serializer):
    name = fields.CharField()
    isoAlphaTwoCode = fields.CharField(source="code")

    class Meta:
        fields = ("name", "isoAlphaTwoCode")
