from rest_framework import generics
from bible.models import Book, Chapter, Verse
from .serializers import BookSerializer, ChapterSerializer, VerseSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ChapterList(generics.ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Chapter.objects.filter(book__id=book_id)

class ChapterDetail(generics.RetrieveAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

class VerseList(generics.ListAPIView):
    serializer_class = VerseSerializer

    def get_queryset(self):
        chapter_id = self.kwargs['chapter_id']
        return Verse.objects.filter(chapter__id=chapter_id)

class VerseDetail(generics.RetrieveAPIView):
    queryset = Verse.objects.all()
    serializer_class = VerseSerializer
