CREATE DATABASE crawler_db
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE crawler_db;

CREATE TABLE crawl_news (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    link TEXT,
    source_url TEXT,
    crawled_at DATETIME NOT NULL
);
