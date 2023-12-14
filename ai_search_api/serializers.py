from rest_framework import serializers

from ai_search_api.search_request import SearchRequest
from ai_search_api.search_result import SearchResult


class SearchRequestSerializer(serializers.Serializer):
    search_phrase = serializers.CharField()

    def create(self, validated_data):
        return SearchRequest(**validated_data)


class SearchResultsSerializer(serializers.ListSerializer):
    name = serializers.CharField()
    description = serializers.CharField()

    def create(self, validated_data):
        models = []
        for model in validated_data:
            models.append(SearchResult(model))
        return models

