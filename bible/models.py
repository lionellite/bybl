from django.db import models
from django.db.models import Q


class Book(models.Model):
    TESTAMENT_CHOICES = (
        ("O", "Ancien"),
        ("N", "Nouveau"),
    )

    idx = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=10)
    testament = models.CharField(max_length=1, choices=TESTAMENT_CHOICES)
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["idx"]
        constraints = [
            models.CheckConstraint(
                condition=Q(idx__gte=1),
                name="book_idx_positive",
            ),
        ]

    def __str__(self):
        return self.name


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    number = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(
                fields=["book", "number"],
                name="unique_chapter_per_book",
            ),
            models.CheckConstraint(
                condition=Q(number__gte=1),
                name="chapter_number_positive",
            ),
        ]

    def __str__(self):
        return f"{self.book} {self.number}"


class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="verses")
    number = models.PositiveSmallIntegerField()
    text = models.TextField()

    class Meta:
        ordering = ["number"]
        constraints = [
            models.UniqueConstraint(
                fields=["chapter", "number"],
                name="unique_verse_per_chapter",
            ),
            models.CheckConstraint(
                condition=Q(number__gte=1),
                name="verse_number_positive",
            ),
        ]

    def __str__(self):
        return f"{self.chapter}:{self.number}"
