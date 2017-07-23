SELECT COLUMN_NAME, CHARACTER_SET_NAME, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS 
  WHERE table_name = 'reddit_posts';

USE arimadb;
ALTER TABLE reddit_posts
  DEFAULT CHARACTER SET utf8mb4,
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;