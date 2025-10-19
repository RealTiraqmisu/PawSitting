from rest_framework import serializers
from snippets.models import Snippet, SnippetCategory


class SnippetCategorySerializer(serializers.ModelSerializer):
    # snippet_set = SnippetSerializer(many=True, read_only=True)

    class Meta:
        model = SnippetCategory
        fields = ['id', 'name', 'snippet_set']

class SnippetSerializer(serializers.ModelSerializer):
    category_detail = SnippetCategorySerializer(source="category", read_only=True)

    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'category', 'category_detail']


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance