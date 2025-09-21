# bible/management/commands/load_bible.py
import json, pathlib
from django.core.management.base import BaseCommand
from django.db import transaction
from bible.models import Book, Chapter, Verse  # ou bible.models

class Command(BaseCommand):
    help = "Charge bible-fr.json dans les trois tables"

    def handle(self, *args, **opts):
        path = pathlib.Path(__file__).resolve().parents[3] / "data" / "bible-fr.json"
        data = json.loads(path.read_text(encoding="utf-8-sig"))

        # Ancien Testament
        for idx, book_json in enumerate(data["Testaments"][0]["Books"], start=1):
            self.save_book(idx, book_json, "O")
        # Nouveau Testament
        for idx, book_json in enumerate(data["Testaments"][1]["Books"], start=40):
            self.save_book(idx, book_json, "N")

    
    def save_book(self, idx, js, testament):
        first_verse_text = js["Chapters"][0]["Verses"][0]["Text"]
        name = first_verse_text.split(" ", 2)[1] if " " in first_verse_text else f"Livre {idx}"

        book, created = Book.objects.update_or_create(
            idx=idx,
            defaults={"name": name, "short_name": name[:4], "testament": testament},
        )
        # on efface l’ancien contenu du livre pour repartir propre
        book.chapters.all().delete()

        for chap_num, chap_js in enumerate(js["Chapters"], start=1):
            c = Chapter.objects.create(book=book, number=chap_num)
            for v_num, v_js in enumerate(chap_js["Verses"], start=1):
                Verse.objects.create(
                    chapter=c,
                    number=v_num,
                    text=v_js["Text"],
                )