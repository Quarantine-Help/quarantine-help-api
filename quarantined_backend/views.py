from rest_framework import views
from rest_framework.response import Response

from quarantined_backend.serializers import CountrySerializerV1


class SupportedCountriesListView(views.APIView):
    def get(self, request, *args, **kwargs):
        from django_countries import countries

        country_data = CountrySerializerV1(countries, many=True)
        return Response({"countries": country_data.data})
