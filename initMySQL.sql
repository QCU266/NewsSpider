CREATE TABLE news_info(
    url VARCHAR(200) NOT NULL,
    post_time DATETIME,
    title VARCHAR(200) NOT NULL,
    keywords VARCHAR(200),
    content TEXT,
    source VARCHAR(100),
    origin VARCHAR(1000),
    PRIMARY KEY(url)
) charset=utf8;
