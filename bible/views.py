from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

from bible.models import Book, Chapter, Verse

SEARCH_PAGE_SIZE = 25
MAX_SEARCH_LENGTH = 100


def home(request):
    books = list(Book.objects.all())
    testament_groups = [
        {
            "label": "Ancien Testament",
            "books": [book for book in books if book.testament == "O"],
        },
        {
            "label": "Nouveau Testament",
            "books": [book for book in books if book.testament == "N"],
        },
    ]
    return render(request, "bible/home.html", {"testament_groups": testament_groups})


def read(request, book_id, chapter=None):
    book = get_object_or_404(Book, idx=book_id)
    chapters = book.chapters.all()
    chapter_number = chapter or 1
    current_chapter = get_object_or_404(chapters, number=chapter_number)
    previous_chapter = chapters.filter(number__lt=chapter_number).last()
    next_chapter = chapters.filter(number__gt=chapter_number).first()

    return render(
        request,
        "bible/read.html",
        {
            "book": book,
            "chapters": chapters,
            "chapter": current_chapter,
            "verses": current_chapter.verses.all(),
            "prev": previous_chapter,
            "next": next_chapter,
        },
    )


def search(request):
    query = request.GET.get("q", "").strip()[:MAX_SEARCH_LENGTH]
    verses = Verse.objects.none()

    if query:
        verses = (
            Verse.objects.filter(Q(text__icontains=query))
            .select_related("chapter__book")
            .order_by("chapter__book__idx", "chapter__number", "number")
        )

    paginator = Paginator(verses, SEARCH_PAGE_SIZE)
    page = paginator.get_page(request.GET.get("page"))
    return render(
        request,
        "bible/search.html",
        {"query": query, "verses": page, "page_obj": page},
    )
