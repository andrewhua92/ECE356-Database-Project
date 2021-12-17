CREATE TABLE hashtag_donaldtrump (
    created_at DATE NOT NULL,
    tweet_id INT NOT NULL,
    tweet VARCHAR(255) NOT NULL,
    likes INT NOT NULL,
    retweet_count INT NOT NULL,
    source VARCHAR(50),
    user_id INT NOT NULL,
    user_name VARCHAR(50),
    user_screen_name VARCHAR(50),
    user_description VARCHAR(255),
    user_join_date DATE NOT NULL,
    user_followers_count INT NOT NULL,
    user_location VARCHAR(255),
    lat DECIMAL(5,2),
    lng DECIMAL(5,2),
    city VARCHAR(255),
    country VARCHAR(255),
    continent VARCHAR(255),
    state VARCHAR(255),
    state_code VARCHAR(2),
    collected_at DATE
);

LOAD DATA LOCAL INFILE 'hashtag_donaldtrump.csv'
INTO TABLE hashtag_donaldtrump
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 500000 ROWS;