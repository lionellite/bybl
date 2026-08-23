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
        return Chapter.objects.filter(book_id=self.kwargs["book_id"])


class ChapterDetail(generics.RetrieveAPIView):
    queryset = Chapter.objects.select_related("book")
    serializer_class = ChapterSerializer


class VerseList(generics.ListAPIView):
    serializer_class = VerseSerializer

    def get_queryset(self):
        return Verse.objects.filter(chapter_id=self.kwargs["chapter_id"]).select_related(
            "chapter__book"
        )


class VerseDetail(generics.RetrieveAPIView):
    queryset = Verse.objects.select_related("chapter__book")
    serializer_class = VerseSerializer
