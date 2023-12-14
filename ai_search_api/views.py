from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from ai_search_api import search_service
from ai_search_api.serializers import SearchRequestSerializer
from pprint import pprint as pp


class Search(APIView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        # pp(request.__dict__)
        req_serializer = SearchRequestSerializer(data=request.data)
        try:
            req_serializer.is_valid()
            search_request = req_serializer.save()

        except ValidationError as e:
            return Response(e.errors, status.HTTP_400_BAD_REQUEST)

        # pp(search_request.__dict__)
        results = search_service.search(search_request.search_phrase)

        return Response(
            results,
            status=status.HTTP_201_CREATED,
        )