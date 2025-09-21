from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from bible.models import Book, Chapter, Verse

def home(request):
    return render(request, "bible/home.html", {"books": Book.objects.all()})

def read(request, book_id, chapter=None):
    book = get_object_or_404(Book, idx=book_id)
    chapters = book.chapters.all()
    if chapter is None:
        chapter = 1
    chap = get_object_or_404(chapters, number=chapter)
    prev_chap = chapters.filter(number__lt=chapter).last()
    next_chap = chapters.filter(number__gt=chapter).first()
    return render(
        request,
        "bible/read.html",
        {
            "book": book,
            "chapters": chapters,
            "chapter": chap,
            "verses": chap.verses.all(),
            "prev": prev_chap,
            "next": next_chap,
        },
    )

def search(request):
    q = request.GET.get("q", "")
    results = []
    if q:
        results = (
            Verse.objects.filter(Q(text__icontains=q))
            .select_related("chapter__book")
            .order_by("chapter__book__idx", "chapter__number", "number")
        )
    return render(request, "bible/search.html", {"query": q, "verses": results})