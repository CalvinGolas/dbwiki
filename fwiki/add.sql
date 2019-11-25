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
    (first, last, birth, death),
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
    (4, 3),

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
    (1, NULL, 5),
