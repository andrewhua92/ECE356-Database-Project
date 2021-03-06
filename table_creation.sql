-- Creating table for the tweet API metadata
CREATE TABLE Tweet (
    created_at DATETIME NOT NULL,
    tweet_id DOUBLE NOT NULL,
    tweet VARCHAR(1000) NOT NULL,
    likes INT NOT NULL DEFAULT 0,
    retweets INT NOT NULL DEFAULT 0,
    source VARCHAR(50),
    user_id DOUBLE NOT NULL,
    user_name VARCHAR(50),
    user_screen_name VARCHAR(50),
    user_description VARCHAR(255),
    user_join_date DATETIME,
    followers INT NOT NULL DEFAULT 0,
    user_location VARCHAR(255),
    lat DECIMAL(5,2),
    lng DECIMAL(5,2),
    city VARCHAR(255),
    country VARCHAR(255),
    continent VARCHAR(255),
    state VARCHAR(255),
    state_code VARCHAR(2),
    collected_at DATETIME,
    PRIMARY KEY (tweet_id)
);

CREATE TABLE Hashtag_donaldtrump (
    created_at DATETIME NOT NULL,
    tweet_id DOUBLE NOT NULL,
    tweet VARCHAR(1000) NOT NULL,
    likes INT NOT NULL DEFAULT 0,
    retweets INT NOT NULL DEFAULT 0,
    source VARCHAR(50),
    user_id DOUBLE NOT NULL,
    user_name VARCHAR(50),
    user_screen_name VARCHAR(50),
    user_description VARCHAR(255),
    user_join_date DATETIME,
    followers INT NOT NULL DEFAULT 0,
    user_location VARCHAR(255),
    lat DECIMAL(5,2),
    lng DECIMAL(5,2),
    city VARCHAR(255),
    country VARCHAR(255),
    continent VARCHAR(255),
    state VARCHAR(255),
    state_code VARCHAR(2),
    collected_at DATETIME,
    party VARCHAR(3),
    PRIMARY KEY (tweet_id),
    FOREIGN KEY (tweet_id) REFERENCES Tweet(tweet_id)
);

CREATE TABLE Hashtag_joebiden (
    created_at DATETIME NOT NULL,
    tweet_id DOUBLE NOT NULL,
    tweet VARCHAR(1000) NOT NULL,
    likes INT NOT NULL DEFAULT 0,
    retweets INT NOT NULL DEFAULT 0,
    source VARCHAR(50),
    user_id DOUBLE NOT NULL,
    user_name VARCHAR(50),
    user_screen_name VARCHAR(50),
    user_description VARCHAR(255),
    user_join_date DATETIME,
    followers INT NOT NULL DEFAULT 0,
    user_location VARCHAR(255),
    lat DECIMAL(5,2),
    lng DECIMAL(5,2),
    city VARCHAR(255),
    country VARCHAR(255),
    continent VARCHAR(255),
    state VARCHAR(255),
    state_code VARCHAR(2),
    collected_at DATETIME,
    party VARCHAR(3),
    PRIMARY KEY (tweet_id),
    FOREIGN KEY (tweet_id) REFERENCES Tweet(tweet_id)
);

-- Loading data for the tweet API metadata
LOAD DATA LOCAL INFILE 'hashtag_donaldtrump.csv'
INTO TABLE Tweet
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
ESCAPED BY '\b'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'hashtag_joebiden.csv'
INTO TABLE Tweet
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
ESCAPED BY '\b'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'hashtag_donaldtrump.csv'
INTO TABLE Hashtag_donaldtrump
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
ESCAPED BY '\b'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(created_at, tweet_id, tweet, likes, retweets, source, user_id, user_name, user_screen_name, user_description, user_join_date,
followers, user_location, lat, lng, city, country, continent, state, state_code, collected_at, @var)
SET party = 'REP';

LOAD DATA LOCAL INFILE 'hashtag_joebiden.csv'
INTO TABLE Hashtag_joebiden
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
ESCAPED BY '\b'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(created_at, tweet_id, tweet, likes, retweets, source, user_id, user_name, user_screen_name, user_description, user_join_date,
followers, user_location, lat, lng, city, country, continent, state, state_code, collected_at, @var)
SET party = 'DEM';

-- Creating table for the 2020 general election data, and previous election data (demographics included for now)
CREATE TABLE County_statistics_all (
    id INT NOT NULL,
    county VARCHAR(255) NOT NULL COLLATE utf8_bin,
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
    Employed INT,
    PrivateWork DECIMAL(3,1),
    PublicWork DECIMAL(3,1),
    SelfEmployed DECIMAL(3,1),
    FamilyWork DECIMAL(3,1),
    Unemployment DECIMAL(3,1)
);

CREATE TABLE County_statistics (
    county VARCHAR(255) NOT NULL COLLATE utf8_bin,
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
    notes VARCHAR(255) DEFAULT "",
    PRIMARY KEY (county, state)
);

CREATE TABLE Demographics (
    county VARCHAR(255) NOT NULL COLLATE utf8_bin,
    state VARCHAR(2) NOT NULL,
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
    Employed INT,
    PrivateWork DECIMAL(3,1),
    PublicWork DECIMAL(3,1),
    SelfEmployed DECIMAL(3,1),
    FamilyWork DECIMAL(3,1),
    Unemployment DECIMAL(3,1),
    PRIMARY KEY (county, state),
    FOREIGN KEY (county, state) REFERENCES County_statistics(county, state)
);

CREATE TABLE Trump_biden_polls (
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
    pollster_rating_name VARCHAR(255),
    fte_grade VARCHAR(2),
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
    pct DECIMAL(4,2),
    PRIMARY KEY (question_id, poll_id, pollster)
);

CREATE TABLE Trump_clinton_polls (
    id INT NOT NULL,
    start_date DATE,
    end_date DATE,
    state VARCHAR(50),
    pollster VARCHAR(255),
    fte_grade VARCHAR(2),
    sample_size INT,
    population VARCHAR(2),
    clinton_pct DECIMAL(4,2),
    trump_pct DECIMAL(4,2),
    dem_lead DECIMAL(6,4),
    PRIMARY KEY (id, pollster)
);

LOAD DATA LOCAL INFILE 'county_statistics.csv'
INTO TABLE County_statistics_all
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

INSERT INTO County_statistics
(county, state, percentage16_Donald_Trump, percentage16_Hillary_Clinton, total_votes16, votes16_Donald_Trump, votes16_Hillary_Clinton,
percentage20_Donald_Trump, percentage20_Joe_Biden, total_votes20, votes20_Donald_Trump, votes20_Joe_Biden, lat, lng)
SELECT county, state, percentage16_Donald_Trump, percentage16_Hillary_Clinton, total_votes16, votes16_Donald_Trump, votes16_Hillary_Clinton,
percentage20_Donald_Trump, percentage20_Joe_Biden, total_votes20, votes20_Donald_Trump, votes20_Joe_Biden, lat, lng 
FROM County_statistics_all;

INSERT INTO Demographics 
(county, state, cases, deaths, TotalPop, Men, Women, Hispanic, White, Black, Native, Asian, Pacific, VotingAgeCitizen, Income, IncomeErr,
IncomePerCap, IncomePerCapErr, Poverty, ChildPoverty, Professional, Service, Office, Construction, Production, Drive, Carpool, Transit,
Walk, OtherTransp, WorkAtHome, MeanCommute, Employed, PrivateWork, PublicWork, SelfEmployed, FamilyWork, Unemployment)
SELECT county, state, cases, deaths, TotalPop, Men, Women, Hispanic, White, Black, Native, Asian, Pacific, VotingAgeCitizen, Income, IncomeErr,
IncomePerCap, IncomePerCapErr, Poverty, ChildPoverty, Professional, Service, Office, Construction, Production, Drive, Carpool, Transit,
Walk, OtherTransp, WorkAtHome, MeanCommute, Employed, PrivateWork, PublicWork, SelfEmployed, FamilyWork, Unemployment
FROM County_statistics_all;

LOAD DATA LOCAL INFILE 'trump_biden_polls.csv'
INTO TABLE Trump_biden_polls
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(question_id, poll_id, cycle, state, pollster_id, pollster, sponsor_ids, sponsors, display_name, pollster_rating_id, pollster_rating_name, fte_grade,
sample_size, population, population_full, methodology, office_type, seat_number, seat_name, start_date, end_date, election_date, sponsor_candidate,
@var24, partisan, @var26, @var27, @var28, created_at, notes, url, stage, race_id, answer, candidate_id, candidate_name, candidate_party, pct)
SET internal = (@var24 = 'true' or @var24 = 'TRUE'),
tracking = (@var26 = 'true' or @var26 = 'TRUE'),
nationwide_batch = (@var27 = 'true' or @var27 = 'TRUE'),
ranked_choice_reallocated = (@var28 = 'true' or @var28 = 'TRUE');

LOAD DATA LOCAL INFILE 'trump_clinton_polls.csv'
INTO TABLE Trump_clinton_polls
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Creating tables for the US 2020 Election Results for the president
CREATE TABLE President_state (
    state VARCHAR(50),
    votes INT,
    PRIMARY KEY (state)
);

-- county names are NOT the same as ones in county_statistics...
CREATE TABLE President_county_candidate (
    state VARCHAR(50),
    county VARCHAR(255) NOT NULL COLLATE utf8_bin,
    candidate VARCHAR(50),
    party VARCHAR(3),
    total_votes INT,
    won BOOLEAN,
    PRIMARY KEY (state, county, candidate),
    FOREIGN KEY (state) REFERENCES President_state(state)
);

CREATE TABLE President_county (
    state VARCHAR(50),
    county VARCHAR(255) NOT NULL COLLATE utf8_bin,
    current_votes INT,
    total_votes INT,
    percent DECIMAL(5,2),
    PRIMARY KEY (state, county),
    FOREIGN KEY (state) REFERENCES President_state(state)
);

LOAD DATA LOCAL INFILE 'president_state.csv'
INTO TABLE President_state
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'president_county_candidate.csv'
INTO TABLE President_county_candidate
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(state, county, candidate, party, total_votes, @var6)
SET won = (@var6 = 'True');

LOAD DATA LOCAL INFILE 'president_county.csv'
INTO TABLE President_county
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
