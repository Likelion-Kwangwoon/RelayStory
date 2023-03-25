from .models import Book,Comment
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["user","cover",'title']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["book","nickname",'content']


