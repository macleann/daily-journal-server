import sqlite3
from models import Mood

def get_all_moods():
    """Returns all moods"""
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Moods m
        """)

        moods = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            mood = Mood(row['id'], row['label'])
            moods.append(mood.__dict__)

    return moods

def get_single_mood(id):
    """Returns a single mood

    Args:
        id (int): id of the mood to retrieve
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Moods m
        WHERE m.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        mood = Mood(data['id'], data['label'])

        return mood.__dict__

def create_mood(new_mood):
    """Adds a new mood

    Args:
        new_mood (dict): mood to be added
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Moods
            ( label )
        VALUES ( ? )
        """, ( new_mood['label'], ))

        id = db_cursor.lastrowid
        new_mood['id'] = id

    return new_mood

def update_mood(id, new_mood):
    """Updates an existing mood

    Args:
        new_mood (dict): the updated mood
        id (int): the id of the mood to be updated
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Moods
            SET
                label = ?
        WHERE id = ?
        """, (new_mood['label'], id ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def delete_mood(id):
    """Deletes a single mood

    Args:
        id (int): Id of mood to be deleted
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Moods
        WHERE id = ?
        """, ( id, ))
