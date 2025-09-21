from rest_framework import serializers
from bible.models import Book, Chapter, Verse

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'idx', 'name', 'description', 'testament']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'number', 'book']

class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'number', 'text', 'chapter']
