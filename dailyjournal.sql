CREATE TABLE Moods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    label TEXT NOT NULL
);

CREATE TABLE Entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    concept TEXT NOT NULL,
    entry TEXT NOT NULL,
    mood_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Moods`(`id`)
);

CREATE TABLE Tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE EntryTags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY(`entry_id`) REFERENCES `Entries`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

INSERT INTO Moods (label) VALUES ('Happy');
INSERT INTO Moods (label) VALUES ('Sad');
INSERT INTO Moods (label) VALUES ('Angry');
INSERT INTO Moods (label) VALUES ('Ok');

INSERT INTO Entries (concept, entry, mood_id, date) VALUES ('Javascript', 'I learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.\nI learned about loops today. They can be a lot of fun.', 1, 'Wed Sep 15 2021 10:10:47 ');
INSERT INTO Entries (concept, entry, mood_id, date) VALUES ('Python', 'Python is named after the Monty Python comedy group from the UK. I''m sad because I thought it was named after the snake', 4, 'Wed Sep 15 2021 10:11:33 ');
INSERT INTO Entries (concept, entry, mood_id, date) VALUES ('Python', 'Why did it take so long for python to have a switch statement? It''s much cleaner than if/elif blocks', 3, 'Wed Sep 15 2021 10:13:11 ');
INSERT INTO Entries (concept, entry, mood_id, date) VALUES ('Javascript', 'Dealing with Date is terrible. Why do you have to add an entire package just to format a date. It makes no sense.', 3, 'Wed Sep 15 2021 10:14:05 ');

INSERT INTO Tags (name) VALUES ('Fun');
INSERT INTO Tags (name) VALUES ('Boring');
INSERT INTO Tags (name) VALUES ('Exciting');
INSERT INTO Tags (name) VALUES ('Confusing');
INSERT INTO Tags (name) VALUES ('Frustrating');
INSERT INTO Tags (name) VALUES ('Easy');