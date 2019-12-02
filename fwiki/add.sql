INSERT INTO User
    (first, last, email, password)
    VALUES
    ('test', 'test2', 'test@gmail.com', 'test');

INSERT INTO Book
    (name, published)
    VALUES
    ('Harry Potter and the Philosophers stone', '1997'),
    ('Harry Potter and the Chamber of Secrets', '1998'),
    ('Harry Potter and the Prisoner of Azkaban', '1999'),
    ('Lord of the rings: The Two Towers', '1968'),
    ('Lord of the rings: Fellowship of the ring', '1968');

INSERT INTO Author
    (first, last, birth, death)
    VALUES
    ('Joanne', 'Rowling','1965-07-31', NULL),
    ('J.R.R', 'Tolkien', '1892-01-03','1973-09-02');

INSERT INTO Chapter
    (bookId, chapterNumber)
    VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (3, 1),
    (3, 2),
    (4, 1),
    (4, 2),
    (4, 3);

INSERT INTO WroteBy
    (book, author)
    VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 2);

INSERT INTO ReadTo
    (user, chapterNumber, book)
    VALUES
    (1, 3, 1),
    (1, 2, 2),
    (1, 1, 3),
    (1, 1, 4),
    (1, NULL, 5);

INSERT INTO Entry
    (title, lastModified)
    VALUES
    ('Harry Potter', CURRENT_TIMESTAMP),
    ('Frodo Baggins', CURRENT_TIMESTAMP),
    ('Voldemort', CURRENT_TIMESTAMP),
    ('Calvin Golas', CURRENT_TIMESTAMP),
    ('Harrison Crisman', CURRENT_TIMESTAMP),
    ('Irvin Choi', CURRENT_TIMESTAMP),
    ('Gandalf', CURRENT_TIMESTAMP),
    ('Tony Stark', CURRENT_TIMESTAMP),
    ('Captain America', CURRENT_TIMESTAMP),
    ('Saruman', CURRENT_TIMESTAMP);

INSERT INTO EntryData
    (entryText, modified, type, entryNumber, chapterNumber, bookId)
    VALUES
    ('This is the protagonist for harry potter.',CURRENT_TIMESTAMP,1,1, 1, 1),
    ('This is the protagonist for harry potter.',CURRENT_TIMESTAMP,2, 1,1, 2),
    ('This is the protagonist for harry potter.',CURRENT_TIMESTAMP,3, 1, 1, 3),
    ('This is the protagonist of Lord of the Rings.',CURRENT_TIMESTAMP,4, 5, 1, 4),
    ('This is the protagonist for Lord of the Rings.',CURRENT_TIMESTAMP,1, 5, 1, 5);

SELECT *
FROM Entry
         INNER JOIN EntryData ON Entry.id = EntryData.entryNumber;
UPDATE EntryData
SET entryText = 'He dies at the end'
WHERE id = 2;