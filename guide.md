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
