import sqlite3
from models import Tag, EntryTag

def get_all_tags():
    """Returns all tags"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.name
        FROM Tags t
        """)

        tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            tag = Tag(row['id'], row['name'])
            tags.append(tag.__dict__)

        return tags

def get_entrytags_by_id(id):
    """Returns all entrytags for a single entry"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id
        FROM EntryTags et
        WHERE et.entry_id = ?
        """, ( id, ))

        entrytags = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entrytag = EntryTag(row['id'], row['entry_id'], row['tag_id'])
            entrytags.append(entrytag.tag_id)

        return entrytags
