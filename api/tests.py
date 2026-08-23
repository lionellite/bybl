from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from bible.models import Book, Chapter, Verse


@override_settings(SECURE_SSL_REDIRECT=False)
class BibleApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            idx=1,
            name="Genèse",
            short_name="Gn",
            testament="O",
        )
        self.chapter = Chapter.objects.create(book=self.book, number=1)

    def test_book_list_is_paginated_and_exposes_short_name(self):
        response = self.client.get(reverse("book-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["short_name"], "Gn")

    def test_chapter_list_is_scoped_to_book(self):
        response = self.client.get(
            reverse("chapter-list", kwargs={"book_id": self.book.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["number"], 1)

    def test_verse_list_is_paginated(self):
        Verse.objects.bulk_create(
            [Verse(chapter=self.chapter, number=n, text=f"Verset {n}") for n in range(1, 52)]
        )

        response = self.client.get(
            reverse("verse-list", kwargs={"chapter_id": self.chapter.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 51)
        self.assertEqual(len(response.data["results"]), 50)
