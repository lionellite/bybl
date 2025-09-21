from django.contrib import admin
from .models import Book, Chapter, Verse

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("idx", "name", "testament")

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("book", "number")

@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ("chapter", "number", "text"[:60])
    search_fields = ("text",)