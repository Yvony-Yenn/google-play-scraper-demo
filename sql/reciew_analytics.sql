CREATE DATABASE review_analytics;
USE review_analytics;

CREATE TABLE apps (
  app_id INT AUTO_INCREMENT PRIMARY KEY,
  package_name VARCHAR(255) NOT NULL UNIQUE,
  app_name VARCHAR(255)
);

CREATE TABLE reviews (
  review_id CHAR(40) PRIMARY KEY,
  app_id INT NOT NULL,
  source VARCHAR(50) NOT NULL DEFAULT 'google_play',
  content TEXT NOT NULL,
  score INT NOT NULL CHECK (score BETWEEN 1 AND 5),
  reviewed_at DATETIME NOT NULL,
  app_version VARCHAR(50),
  user_name VARCHAR(255),
  thumbs_up_count INT DEFAULT 0,
  FOREIGN KEY (app_id) REFERENCES apps(app_id)
);

CREATE INDEX idx_reviews_app_time ON reviews(app_id, reviewed_at);
CREATE INDEX idx_reviews_score ON reviews(score);
CREATE INDEX idx_reviews_version ON reviews(app_version);

