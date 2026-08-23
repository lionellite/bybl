import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from bible.models import Book, Chapter, Verse


BOOKS = (
    ("Genèse", "Gn"),
    ("Exode", "Ex"),
    ("Lévitique", "Lv"),
    ("Nombres", "Nb"),
    ("Deutéronome", "Dt"),
    ("Josué", "Jos"),
    ("Juges", "Jg"),
    ("Ruth", "Rt"),
    ("1 Samuel", "1S"),
    ("2 Samuel", "2S"),
    ("1 Rois", "1R"),
    ("2 Rois", "2R"),
    ("1 Chroniques", "1Ch"),
    ("2 Chroniques", "2Ch"),
    ("Esdras", "Esd"),
    ("Néhémie", "Ne"),
    ("Esther", "Est"),
    ("Job", "Jb"),
    ("Psaumes", "Ps"),
    ("Proverbes", "Pr"),
    ("Ecclésiaste", "Ec"),
    ("Cantique des cantiques", "Ct"),
    ("Ésaïe", "Es"),
    ("Jérémie", "Jr"),
    ("Lamentations", "Lm"),
    ("Ézéchiel", "Ez"),
    ("Daniel", "Dn"),
    ("Osée", "Os"),
    ("Joël", "Jl"),
    ("Amos", "Am"),
    ("Abdias", "Ab"),
    ("Jonas", "Jon"),
    ("Michée", "Mi"),
    ("Nahum", "Na"),
    ("Habacuc", "Ha"),
    ("Sophonie", "So"),
    ("Aggée", "Ag"),
    ("Zacharie", "Za"),
    ("Malachie", "Ml"),
    ("Matthieu", "Mt"),
    ("Marc", "Mc"),
    ("Luc", "Lc"),
    ("Jean", "Jn"),
    ("Actes", "Ac"),
    ("Romains", "Rm"),
    ("1 Corinthiens", "1Co"),
    ("2 Corinthiens", "2Co"),
    ("Galates", "Ga"),
    ("Éphésiens", "Ep"),
    ("Philippiens", "Ph"),
    ("Colossiens", "Col"),
    ("1 Thessaloniciens", "1Th"),
    ("2 Thessaloniciens", "2Th"),
    ("1 Timothée", "1Tm"),
    ("2 Timothée", "2Tm"),
    ("Tite", "Tt"),
    ("Philémon", "Phm"),
    ("Hébreux", "He"),
    ("Jacques", "Jc"),
    ("1 Pierre", "1P"),
    ("2 Pierre", "2P"),
    ("1 Jean", "1Jn"),
    ("2 Jean", "2Jn"),
    ("3 Jean", "3Jn"),
    ("Jude", "Jd"),
    ("Apocalypse", "Ap"),
)


class Command(BaseCommand):
    help = "Charge data/bible-fr.json dans les tables Book, Chapter et Verse."

    def handle(self, *args, **options):
        path = Path(__file__).resolve().parents[3] / "data" / "bible-fr.json"
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except FileNotFoundError as exc:
            raise CommandError(f"Fichier introuvable : {path}") from exc
        except json.JSONDecodeError as exc:
            raise CommandError(f"JSON invalide dans {path} : {exc}") from exc

        testaments = data.get("Testaments")
        if not isinstance(testaments, list) or len(testaments) != 2:
            raise CommandError("Le JSON doit contenir exactement deux testaments.")

        book_count = sum(len(testament.get("Books", [])) for testament in testaments)
        if book_count != len(BOOKS):
            raise CommandError(
                f"Nombre de livres inattendu : {book_count} (attendu : {len(BOOKS)})."
            )

        imported_chapters = 0
        imported_verses = 0
        book_index = 0
        with transaction.atomic():
            for testament_code, testament in zip(("O", "N"), testaments):
                for book_json in testament["Books"]:
                    name, short_name = BOOKS[book_index]
                    chapters, verses = self.save_book(
                        book_index + 1,
                        book_json,
                        testament_code,
                        name,
                        short_name,
                    )
                    imported_chapters += chapters
                    imported_verses += verses
                    book_index += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import terminé : {len(BOOKS)} livres, "
                f"{imported_chapters} chapitres et {imported_verses} versets."
            )
        )

    def save_book(self, idx, data, testament, name, short_name):
        chapters_data = data.get("Chapters") or []
        if not chapters_data:
            raise CommandError(f"Le livre {name} ne contient aucun chapitre.")

        book, _ = Book.objects.update_or_create(
            idx=idx,
            defaults={
                "name": name,
                "short_name": short_name,
                "testament": testament,
                "description": "",
            },
        )
        book.chapters.all().delete()

        chapters = Chapter.objects.bulk_create(
            [Chapter(book=book, number=chapter_number) for chapter_number, _ in enumerate(chapters_data, 1)]
        )
        verses = [
            Verse(chapter=chapter, number=verse_number, text=verse_data.get("Text", ""))
            for chapter, chapter_data in zip(chapters, chapters_data)
            for verse_number, verse_data in enumerate(chapter_data.get("Verses", []), 1)
        ]
        Verse.objects.bulk_create(verses, batch_size=1000)
        return len(chapters), len(verses)
