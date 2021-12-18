-- Creating table for the tweet API metadata
CREATE TABLE hashtag_donaldtrump (
    created_at DATETIME NOT NULL,
    tweet_id DOUBLE NOT NULL,
    tweet VARCHAR(1000) NOT NULL,
    likes INT NOT NULL,
    retweet_count INT,
    source VARCHAR(50),
    user_id DOUBLE NOT NULL,
    user_name VARCHAR(50),
    user_screen_name VARCHAR(50),
    user_description VARCHAR(255),
    user_join_date DATETIME,
    user_followers_count INT,
    user_location VARCHAR(255),
    lat DECIMAL(5,2),
    lng DECIMAL(5,2),
    city VARCHAR(255),
    country VARCHAR(255),
    continent VARCHAR(255),
    state VARCHAR(255),
    state_code VARCHAR(2),
    collected_at DATETIME
);

CREATE TABLE hashtag_joebiden (
    created_at DATETIME NOT NULL,
    tweet_id DOUBLE NOT NULL,
    tweet VARCHAR(1000) NOT NULL,
    likes INT NOT NULL,
    retweet_count INT,
    source VARCHAR(50),
    user_id DOUBLE NOT NULL,
    user_name VARCHAR(50),
    user_screen_name VARCHAR(50),
    user_description VARCHAR(255),
    user_join_date DATETIME,
    user_followers_count INT,
    user_location VARCHAR(255),
    lat DECIMAL(5,2),
    lng DECIMAL(5,2),
    city VARCHAR(255),
    country VARCHAR(255),
    continent VARCHAR(255),
    state VARCHAR(255),
    state_code VARCHAR(2),
    collected_at DATETIME
);

-- Loading data for the tweet API metadata
LOAD DATA LOCAL INFILE 'hashtag_donaldtrump.csv'
INTO TABLE hashtag_donaldtrump
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'hashtag_joebiden.csv'
INTO TABLE hashtag_joebiden
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Creating table for the 2020 general election data, and previous election data (demographics included for now)
CREATE TABLE county_statistics (
    id INT NOT NULL,
    county VARCHAR(255) NOT NULL,
    state VARCHAR(2) NOT NULL,
    percentage16_Donald_Trump DECIMAL(4,3),
    percentage16_Hillary_Clinton DECIMAL(4,3),
    total_votes16 INT,
    votes16_Donald_Trump INT,
    votes16_Hillary_Clinton INT,
    percentage20_Donald_Trump DECIMAL(4,3),
    percentage20_Joe_Biden DECIMAL(4,3),
    total_votes20 INT,
    votes20_Donald_Trump INT,
    votes20_Joe_Biden INT,
    lat DECIMAL(5,2),
    lng DECIMAL(5,2),
    cases INT,
    deaths INT,
    TotalPop INT,
    Men INT,
    Women INT,
    Hispanic DECIMAL(3,1),
    White DECIMAL(3,1),
    Black DECIMAL(3,1),
    Native DECIMAL(3,1),
    Asian DECIMAL(3,1),
    Pacific DECIMAL(3,1),
    VotingAgeCitizen INT,
    Income DECIMAL(9,2),
    IncomeErr DECIMAL(6,2),
    IncomePerCap DECIMAL(9,2),
    IncomePerCapErr DECIMAL(6,2),
    Poverty DECIMAL(3,1),
    ChildPoverty DECIMAL (3,1),
    Professional DECIMAL(3,1),
    Service DECIMAL(3,1),
    Office DECIMAL(3,1),
    Construction DECIMAL(3,1),
    Production DECIMAL(3,1),
    Drive DECIMAL(3,1),
    Carpool DECIMAL(3,1),
    Transit DECIMAL(3,1),
    Walk DECIMAL(3,1),
    OtherTransp DECIMAL(3,1),
    WorkAtHome DECIMAL(3,1),
    MeanCommute DECIMAL(3,1),
    Employed DECIMAL(3,1),
    PrivateWork DECIMAL(3,1),
    PublicWork DECIMAL(3,1),
    SelfEmployed DECIMAL(3,1),
    FamilyWork DECIMAL(3,1),
    Unnemployment DECIMAL(3,1)
);

CREATE TABLE trump_biden_polls (
    question_id INT NOT NULL,
    poll_id INT NOT NULL,
    cycle INT,
    state VARCHAR(50),
    pollster_id INT NOT NULL,
    pollster VARCHAR(255),
    sponsor_ids INT,
    sponsors VARCHAR(255),
    display_name VARCHAR(255),
    pollster_rating_id INT NOT NULL,
    polster_rating_name VARCHAR(255),
    fte_grade VARCHAR(1),
    sample_size INT,
    population VARCHAR(2),
    population_full VARCHAR(2),
    methodology VARCHAR(50),
    office_type VARCHAR(20), -- static...
    seat_number INT, -- static ...
    seat_name VARCHAR(1), -- empty??
    start_date DATE,
    end_date DATE,
    election_date DATE,
    sponsor_candidate VARCHAR(50),
    internal BOOLEAN,
    partisan VARCHAR(10),
    tracking BOOLEAN,
    nationwide_batch BOOLEAN, -- static
    ranked_choice_reallocated BOOLEAN, -- static
    created_at DATETIME,
    notes VARCHAR(255), -- not useful
    url VARCHAR(255),
    stage VARCHAR(10), -- static
    race_id INT,
    answer VARCHAR(10), -- try and make this enum?
    candidate_id INT NOT NULL,
    candidate_name VARCHAR(50),
    candidate_party VARCHAR(5),
    pct DECIMAL(4,2)
);

LOAD DATA LOCAL INFILE 'county_statistics.csv'
INTO TABLE county_statistics
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'trump_biden_polls.csv'
INTO TABLE trump_biden_polls
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
