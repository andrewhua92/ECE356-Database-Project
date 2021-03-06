# Elections 2020 Project Setup

## Prerequisite
Download Docker and ensure WSL is updated. Ensure the version of WSL is WSL2.\
If you have WSL but not WSL2 after checking with `wsl.exe -l -v`, follow steps 4 and 5 of the [WSL Installation](https://docs.microsoft.com/en-ca/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)\
If you don't have WSL installed, follow steps 4-6 of the installation.

## Mysql Container Setup
To setup the Mysql instance within docker run the following in WSL/terminal:\
`docker pull mysql:latest`\
`docker run --name=ece356_db --env="MYSQL_ROOT_PASSWORD=root_password" -p 3306:3306 -d mysql:latest`


`docker exec -it ece356_db mysql --local-infile=1 -u root -p`\
[Source](https://medium.com/swlh/how-to-connect-to-mysql-docker-from-python-application-on-macos-mojave-32c7834e5afa)

When prompted for password, please use `root_password`.

Within the MySQL instance, please run these to create a new database and user:\
`mysql> CREATE DATABASE test_db;`\
`mysql> use test_db`\
`mysql> CREATE USER 'user1' IDENTIFIED BY 'password';`\
`mysql> GRANT ALL PRIVILEGES on test_db.* to 'user1';`

User: `user1`\
Password: `password`

## Loading Mysql DB
Please note, you have to download the following .csv's from Kaggle:\
https://www.kaggle.com/manchunhui/us-election-2020-tweets \
hashtag_donaldtrump.csv\
hashtag_joebiden.csv\
https://www.kaggle.com/etsc9287/2020-general-election-polls \
county_statistics.csv\
trump_biden_polls.csv\
trump_clinton_polls.csv\
https://www.kaggle.com/unanimad/us-election-2020 \
president_county_candidate.csv\
president_county.csv\
president_state.csv

You can also run the script to download the CSVs. Before doing this, please run the following export commands.\
`export KAGGLE_USERNAME=andrewhua90`\
`export KAGGLE_KEY=a3c022f62ad2fb27456311be107d29d6`

The downloading script can be run as follows:\
`bash kaggle_download.txt`

We need to copy over files onto the Docker container. Here's a copying files over example:
`docker cp hashtag_donaldtrump.csv <name_of_container>:/hashtag_donaldtrump.csv`

This needs to be done as the files do not exist locally within the Docker instance.
This can be done quickly  however using our Docker script called `docker_cp_script.txt`, i.e.:
`bash docker_cp_script.txt`

To run the table creation queries, while in the MySQL instance, please run this:
`mysql> source table_creation.sql`/

If you get the following error message: `ERROR 3948 (42000): Loading local data is disabled; this must be enabled on both the client and server sides`\
You can fix this issue by running\
`mysql> SET GLOBAL local_infile=1;`\
`mysql> quit`\
`docker exec -it ece356_db mysql --local-infile=1  -u root -p`\

Now run the table_creation.sql again.


Viewing a row to verify proper insertion (MySQL query):
`SELECT * FROM <table_name> LIMIT 3 \G`

This will bring a vertical view that will be significantly easier to read considering the large number of columns,
and the additional overhead of burdensome string lengths.

Accessing directory of Docker container to verify contents:
`docker exec -it ece356_db /bin/bash`

# Sample Commands for the Application

The core of every command requires an action. The following actions are allowed:
`winner`, `loser`, `demographics`, `polling`, `tweets`, `annotate`, `county`, `state`.
They will vary in different needed flags to supplement the action.

If you would like to know which state refers to which abbreviation (as our commands take in abbreviations only), please refer to the file `US_states.json`.
## Flags
`-s, --state: State that you want to reference (please use abbreviation, i.e. NY for New York)`\
`-c, --county: County that you want to reference (please use full name i.e. Broward)`\
`-p, --presidental_candidate: Candidate that you want to know about. Please use 'jb' for Joe Biden or 'dt' for Donald Trump`\
`-g, --granular: Granular properties when searching up tweets information, demographics, and more.`\
`-d, --date: 2nd half of the queried year for polling data, i.e. 16 for 2016, 20 for 2020`\
`-n, --note: Used to append annotations to a county to be stored in the database.`\
`-r, --remove: Pass this flag when performing the 'annotate' action to remove it entirely.`

## Winner (or Loser) in a State
`python3 app.py winner -s NY`\
`python3 app.py loser -s IL`

The two above commands will show the respective winner (or loser) in the specified state during the US 2020 election.
You must specify the state in order for the action to succeed.

## Tweets Metadata

Possible granular options for `-g` flag are: `likes`, `retweets`, `followers`, where they search for *most* of the specific option in a tweet given the parameters of the command.

`python3 app.py tweets -g retweets -p dt`

This will show tweet information including the tweet, the number of retweets, who it was by, and where the tweet was made from (if possible to determine), about the specified candidate.


`python3 app.py tweets -s NY -p jb`

This will show the number of tweets about the specified candidate in the specified state.

`python3 app.py tweets -s IL -p dt -g likes`

This will show tweet information including the tweet, the number of likes, who it was by, and where the tweet was made from (if possible to determine), all from the specified state about the specified candidate.

## Demographics

Possible granular options for `-g` flags are: `cases`, `deaths`, `men`, `women`, `hispanic`, `white`, `black`, `native`, `asian`, `pacific`, `poverty`, `childPoverty`, `votingAgeCitizen`, `income`, `incomeerr`, `incomepercap`, `incomepercaperr` `professional`, `service`,  `office`, `construction`, `production`, `drive`, `carpool`, `transit`, `walk`, `otherTransp`, `workAtHome`, `meanCommute`, `employed`,`privateWork`,`publicWork`,`selfEmployed`,`familyWork`,`unemployment`

Note that you can only use one at a time. The command will output statistics about that demographic, and also supplement it with differential data from the previous election to see how it (may) have affected turnout.

`python3 app.py demographics -s FL -g drive`

This will show statistics on how much of the specified demographic represented the total votes in the specified state. It will also be supplemented with average percentage of votes and average number of votes and the average differences of the two aforementioned averages between 2016 and 2020. 

## Polling

The flag used for polling is `-d`, where you can specify either the 2020 election with '20' or 2016 election with '16'. By default, it will use '20'. It also uses `-s` for the specified state.

`python3 app.py polling -s AK -d 16`

This will show stats for the number of votes for *polls* in the 2016 election prior to the actual election in Alaska. This shows votes for Donald Trump and Hillary Clinton.

`python3 app.py polling -s NV`

This will show stats for the number of votes for *polls* in the 2020 election prior to the actual election in Nevada. This shows votes for the top 3 candidates in descending order (typically Trump and Biden round out the first two candidates, with the third candidate shown for interest).

## Annotate

You can either choose to add an annotation using `-n` and the annotation immediately following it, or remove the annotation. You must also specify the county name and the state of the county thaT you wish to add an annotation to. Note that annotations are limited to 255 characters.

`python3 app.py annotate -s NY -c Queens -n "Very popular location!"`

This will add the string 'Very popular location!' to the county called Queens located in New York.

`python3 app.py annotate -s NY -c Queens -r`

This will reverse (effectively erase the note) attached to the county called Queens located in New York.

## County

Allows user to search specific information about a county, whether in general, demographics-related, historic in votes related, or all of the above. The `-g` granularity options are `demographics`, `historic`, `all` for the corresponding amount of information, with no `-g` flag at all for general information.

`python3 app.py county -s LA -c Acadia`

This will provide surface level information about the county such as longitutde and latitutde, and any annotations.

`python3 app.py county -c Anchorage -s AK -g demographics`

This will provide demographic related information in the county of Anchorage in the state of Alaska.

## State

Allows user to search specific information about a state, whether it is demographics-related, historic in votes related, or both of the above. The `-g` granularity options are `demographics`, `historic`, `all` for the corresponding amount of information. This must be passed with a `-g` flag.

`python3 app.py state -s IN -g historic`

This will provide the historic voting information about Indiana (averaged or summed across all the counties in the state).
