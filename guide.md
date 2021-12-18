Download Docker. Ensure WSL is updated. Ensure WSL is WSL2, otherwise, go convert it.

`docker pull mysql:latest`
`docker run --name=ece356_db --env="MYSQL_ROOT_PASSWORD=root_password" -p 3306:3306 -d mysql:latest`

https://medium.com/swlh/how-to-connect-to-mysql-docker-from-python-application-on-macos-mojave-32c7834e5afa

`docker exec -it ece356_db mysql --local-infile=1 -u root -p`
`docker exec -it <name_of_container> mysql --local-infile=1 -u root -p`

Within the MySQL instance, please run these to create a new database and user:
`mysql> CREATE DATABASE test_db;`
`mysql> use test_db`
`mysql> CREATE USER 'user1' IDENTIFIED BY 'password';`
`mysql> GRANT ALL PRIVILEGES on test_db.* to 'user1';`

User: `user1`
Password: `password`

Please note, you have to download the following .csv's from Kaggle:
https://www.kaggle.com/manchunhui/us-election-2020-tweets
hashtag_donaldtrump.csv
hashtag_joebiden.csv
https://www.kaggle.com/etsc9287/2020-general-election-polls
county_statistics.csv
trump_biden_polls.csv
trump_clinton_polls.csv
https://www.kaggle.com/unanimad/us-election-2020
president_county_candidate.csv
president_county.csv
president_state.csv

You can also run the script to downloads. Before doing this, please run the following export commands.
`export KAGGLE_USERNAME=andrewhua90`
`export KAGGLE_KEY=91db567e6efba3e4b746b5b77a28728e`

Copying files over example:
`docker cp hashtag_donaldtrump.csv <name_of_container>:/hashtag_donaldtrump.csv`

This needs to be done as the files do not exist locally within the Docker instance.
This can be done quickly  however using our Docker script called `docker_cp_script.txt`, i.e.:
`bash docker_cp_script.txt`

To run the table creation queries, while in the MySQL instance, please run this:
`mysql> source table_creation.sql`

Viewing a row to verify proper insertion (MySQL query):
`SELECT * FROM <table_name> LIMIT 3 \G`

This will bring a vertical view that will be significantly easier to read considering the large number of columns,
and the additional overhead of burdensome string lengths.

Accessing directory of Docker container to verify contents:
`docker exec -it <name_of_container> /bin/bash`
`docker exec -it ece356_db /bin/bash`