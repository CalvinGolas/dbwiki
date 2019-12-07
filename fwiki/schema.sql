DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Entry;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Author;
DROP TABLE IF EXISTS Chapter;
DROP TABLE IF EXISTS EntryData;
DROP TABLE IF EXISTS WroteBy;
DROP TABLE IF EXISTS ReadTo;
DROP TABLE IF EXISTS Types;

-- User table:
CREATE TABLE User (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	first VARCHAR(50) NOT NULL,
	last VARCHAR(50) NOT NULL,
	email VARCHAR(150) UNIQUE NOT NULL,
	password VARCHAR(50) NOT NULL
);

-- Entry table:
CREATE TABLE Entry (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title VARCHAR(100) NOT NULL,
	imageLocation VARCHAR(150),
	lastModified TIMESTAMP NOT NULL
);

-- Book table:
CREATE TABLE Book (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(150) NOT NULL
);

-- Author table:
CREATE TABLE Author (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	first VARCHAR(50) NOT NULL,
	last VARCHAR(50) NOT NULL,
	birth DATE NOT NULL,
	death DATE
);

-- Chapter table:
CREATE TABLE Chapter (
	bookId INTEGER,
	chapterNumber INTEGER,
	PRIMARY KEY (bookId, chapterNumber),
    FOREIGN KEY (bookId) REFERENCES Book(id)
);

-- EntryData table:
CREATE TABLE EntryData (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	entryText TEXT NOT NULL,
	modified DATETIME NOT NULL,
	type INT NOT NULL,
	entryNumber INT NOT NULL,
	chapterNumber INT NOT NULL,
	bookId INT NOT NULL,
    FOREIGN KEY (type) REFERENCES Types(type),
	FOREIGN KEY (entryNumber) REFERENCES Entry(id),
	FOREIGN KEY (chapterNumber, bookId) REFERENCES Chapter(chapterNumber, bookId)
);

CREATE TABLE Types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type VARCHAR(50)
);
INSERT INTO Types (type) VALUES
    ('description'), ('attributes'), ('trivia'), ('references');


-- WroteBy table:
CREATE TABLE WroteBy (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	book INT,
	author INT NOT NULL,
    FOREIGN KEY (book) REFERENCES Book(id),
	FOREIGN KEY (author) REFERENCES Author(id)
);

-- ReadTo table:
CREATE TABLE ReadTo (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user INT,
	chapterNumber INT,
	book INT NOT NULL,
    FOREIGN KEY (chapterNumber, book) REFERENCES Chapter(chapterNumber, bookId),
	FOREIGN KEY (user) REFERENCES User(id)
);


