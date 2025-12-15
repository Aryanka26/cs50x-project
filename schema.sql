-- schema.sql
-- Database schema for Book Review Web App

-- Drop old tables if they exist.
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;

-- USERS TABLE
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
            hash TEXT NOT NULL
            );

            -- BOOKS TABLE
            CREATE TABLE books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                        author TEXT NOT NULL,
                            year INTEGER,
                                isbn TEXT NOT NULL UNIQUE
                                );

                                -- Add an index for faster searching by title/author/ISBN
                                CREATE INDEX idx_books_title ON books(title);
                                CREATE INDEX idx_books_author ON books(author);
                                CREATE INDEX idx_books_isbn ON books(isbn);

                                -- REVIEWS TABLE
                                CREATE TABLE reviews (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        user_id INTEGER NOT NULL,
                                            book_id INTEGER NOT NULL,
                                                rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                                                    comment TEXT,
                                                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                                                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                                                                FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
                                                                    UNIQUE (user_id, book_id) -- each user can review a book only once
                                                                    );

                                                                    -- Add indexes for performance
                                                                    CREATE INDEX idx_reviews_user ON reviews(user_id);
                                                                    CREATE INDEX idx_reviews_book ON reviews(book_id);
                                                                    