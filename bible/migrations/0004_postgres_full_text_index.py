from django.db import migrations


INDEX_NAME = "bible_verse_text_search_idx"


def add_postgres_index(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute(
        f"CREATE INDEX IF NOT EXISTS {INDEX_NAME} "
        "ON bible_verse USING GIN (to_tsvector('french', text))"
    )


def remove_postgres_index(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute(f"DROP INDEX IF EXISTS {INDEX_NAME}")


class Migration(migrations.Migration):
    dependencies = [
        ("bible", "0003_alter_chapter_unique_together_and_more"),
    ]

    operations = [
        migrations.RunPython(add_postgres_index, remove_postgres_index),
    ]
