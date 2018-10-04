CREATE TABLE comment_number (
    highest BIGINT NOT NULL DEFAULT 221534646352
);

CREATE TABLE comments (
    id INTEGER,
    name VARCHAR(80) NOT NULL,
    link VARCHAR(300) NOT NULL,
    comment VARCHAR (500) NOT NULL,
    timestamp VARCHAR(80) NOT NULL,
    PRIMARY KEY (id)
);