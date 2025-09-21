from django.db import models

class Book(models.Model):
    idx        = models.PositiveSmallIntegerField(unique=True)  # 1=Genèse …
    name       = models.CharField(max_length=30)
    short_name = models.CharField(max_length=10)               # Gn, Ex …
    testament = models.CharField(max_length=1, choices=[("O","Ancien"),("N","Nouveau")])
    description = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["idx"]

    def __str__(self):
        return self.name


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="chapters")
    number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("book", "number")
        ordering = ["number"]

    def __str__(self):
        return f"{self.book} {self.number}"


class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="verses")
    number  = models.PositiveSmallIntegerField()
    text    = models.TextField()

    class Meta:
        unique_together = ("chapter", "number")
        ordering = ["number"]

    def __str__(self):
        return f"{self.chapter}:{self.number}"