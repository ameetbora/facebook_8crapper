CREATE TABLE comment_number (
    highest BIGINT NOT NULL DEFAULT 221534646352
);

CREATE TABLE comments (
    id SERIAL,
    user_id INTEGER,
    comment VARCHAR (5000) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    UNIQUE(comment, timestamp, user_id)
);

CREATE TABLE users (
    id SERIAL,
    name VARCHAR(80) NOT NULL,
    link VARCHAR(300) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE(name, link)
);


INSERT INTO users (name, link) VALUES ({name}, {link})
WHERE NOT EXISTS (
    SELECT id
    FROM users
    WHERE name = {name} AND link = {link}
    )
returning id