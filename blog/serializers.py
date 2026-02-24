from rest_framework import serializers
from .models import Blog , Comment

class BlogSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    like_count = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = '__all__'

    def get_like_count(self, obj):
        return obj.likes.count()

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'