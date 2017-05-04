from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('username', 'text', 'content_url')


class DevCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=200)
    text = serializers.CharField()
    content_url = serializers.CharField(max_length=200)
    ip = serializers.CharField(max_length=200, write_only=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        validated_data.pop('ip', None)
        return Comment.objects.create(**validated_data)
    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.username= validated_data.get('username', instance.username)
        instance.text = validated_data.get('text', instance.text)
        instance.content_url = validated_data.get('text', instance.content_url)
        instance.save()
        return instance
