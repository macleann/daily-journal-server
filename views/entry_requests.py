import sqlite3
from models import Entry, Mood, Tag

def get_all_entries():
    """Returns all entries"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            m.label,
            e.date
        FROM Entries e
        JOIN Moods m ON m.id = e.mood_id
        """)

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'],
                          row['mood_id'], row['date'])

            mood = Mood(row['mood_id'], row['label'])

            entry.mood = mood.__dict__

            # Find the current id for the entry row we're in
            current_id = entry.id
            # Query the database, we only want whatever matches the current entry
            db_cursor.execute("""
            SELECT * FROM Tags t
            JOIN EntryTags et ON et.tag_id = t.id
            JOIN Entries e ON e.id = et.entry_id
            WHERE et.entry_id = ?
            """, ( current_id, ))
            # Create an empty list to hold tags down the line
            tags = []
            # Variable naming is confusing and fun
            subset = db_cursor.fetchall()
            # Iterate through the SQL we just queried
            for row in subset:
                # Hey, this is what a tag looks like
                tag = Tag(row['id'], row['name'])
                # We only need the id's for the tags list we made earlier
                tags.append(tag.id)
            # Give the current entry a key of tags and value of the tags list we just populated
            entry.tags = tags

            entries.append(entry.__dict__)

        return entries

def get_single_entry(id):
    """Returns a single entry

    Args:
        id (int): Id of the entry
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.mood_id,
            m.label,
            e.date
        FROM Entries e
        JOIN Moods m ON m.id = e.mood_id
        WHERE e.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        entry = Entry(data['id'], data['concept'], data['entry'],
                    data['mood_id'], data['date'])

        mood = Mood(data['mood_id'], data['label'])

        entry.mood = mood.__dict__

        return entry.__dict__

def get_queried_entries(query):
    """Returns all entries containing a certain word

    Args:
        query (str): word to find
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry, 
            e.mood_id,
            m.label,
            e.date
        FROM Entries e
        JOIN Moods m ON m.id = e.mood_id
        WHERE e.entry LIKE ?
        """, ( f'%{query}%', ))

        entries = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'],
                          row['mood_id'], row['date'])

            mood = Mood(row['mood_id'], row['label'])

            entry.mood = mood.__dict__

            entries.append(entry.__dict__)

    return entries

def create_entry(new_entry):
    """Creates a new entry

    Args:
        new_entry (dict): New entry to be added
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entries
            ( concept, entry, mood_id, date )
        VALUES
            ( ? , ? , ? , ? )
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date']))

        id = db_cursor.lastrowid
        new_entry['id'] = id

        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO EntryTags
                ( entry_id, tag_id )
            VALUES
                ( ? , ? )
            """, (new_entry['id'], tag))

    return new_entry

def update_entry(id, new_entry):
    """Updates an entry

    Args:
        new_entry (dict): The updated entry
        id (int): The id of the entry to be updated
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Entries
            SET
                concept = ?,
                entry = ?,
                mood_id = ?,
                date = ?
        WHERE id = ?
        """, (new_entry['concept'], new_entry['entry'], new_entry['mood_id'], new_entry['date'], id, ))

        db_cursor.execute("""
        DELETE FROM EntryTags
        WHERE entry_id = ?
        """, ( id, ))

        for tag in new_entry['tags']:
            db_cursor.execute("""
            INSERT INTO EntryTags
                ( entry_id, tag_id )
            VALUES
                ( ? , ? )
            """, (id, tag))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def delete_entry(id):
    """Deletes a single entry

    Args:
        id (int): Id of the entry
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entries
        WHERE id = ?
        """, ( id, ))
