CREATE TABLE news_info(
    url VARCHAR(100) NOT NULL,
    post_time DATETIME,
    title VARCHAR(100) NOT NULL,
    source VARCHAR(100),
    filename VARCHAR(200),
    keywords VARCHAR(200),
    origin VARCHAR(200),
    PRIMARY KEY(url)
) charset=utf8;
