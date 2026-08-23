from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Book, Chapter, Verse


@override_settings(SECURE_SSL_REDIRECT=False)
class BiblePagesTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            idx=1,
            name="Genèse",
            short_name="Gn",
            testament="O",
            description="Le commencement.",
        )
        self.chapter = Chapter.objects.create(book=self.book, number=1)

    def test_home_lists_books(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Genèse")
        self.assertContains(response, "Ancien Testament")

    def test_read_page_links_verse_anchor(self):
        Verse.objects.create(chapter=self.chapter, number=1, text="Au commencement.")

        response = self.client.get(reverse("read", args=[self.book.idx]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="verset-1"')
        self.assertContains(response, "Au commencement.")

    def test_read_unknown_chapter_returns_404(self):
        response = self.client.get(reverse("read_chap", args=[self.book.idx, 99]))

        self.assertEqual(response.status_code, 404)

    def test_search_escapes_verse_text(self):
        Verse.objects.create(
            chapter=self.chapter,
            number=1,
            text="<script>alert('xss')</script> lumière",
        )

        response = self.client.get(reverse("search"), {"q": "lumière"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;")
        self.assertNotContains(response, "<script>alert('xss')</script>")

    def test_search_is_paginated(self):
        Verse.objects.bulk_create(
            [Verse(chapter=self.chapter, number=n, text=f"mot {n}") for n in range(1, 27)]
        )

        first_page = self.client.get(reverse("search"), {"q": "mot"})
        second_page = self.client.get(reverse("search"), {"q": "mot", "page": 2})

        self.assertEqual(first_page.status_code, 200)
        self.assertContains(first_page, "Page 1 sur 2")
        self.assertContains(second_page, "Page 2 sur 2")
