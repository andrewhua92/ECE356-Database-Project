Download Docker. Ensure WSL is updated. Ensure WSL is WSL2, otherwise, go convert it.

`docker pull mysql:latest`
`docker run --name=ece356_db --env="MYSQL_ROOT_PASSWORD=root_password" -p 3306:3306 -d mysql:latest`

https://medium.com/swlh/how-to-connect-to-mysql-docker-from-python-application-on-macos-mojave-32c7834e5afa

`docker exec -it ece356_db mysql --local-infile=1 -u root -p`
`docker exec -it <name_of_container> mysql --local-infile=1 -u root -p`

User: `user1`
Password: `password`

Copying files over example:
`docker cp hashtag_donaldtrump.csv <name_of_container>:/hashtag_donaldtrump.csv`

This needs to be done as the files do not exist locally within the Docker instance.
This can be done quickly however using our Docker script called `docker_cp_script.sh`, i.e.:
`sh docker_cp_script.sh`

Viewing a row to verify proper insertion (MySQL query):
`SELECT * FROM <table_name> LIMIT 3 \G`

This will bring a vertical view that will be significantly easier to read considering the large number of columns,
and the additional overhead of burdensome string lenghts.

Accessing directory of Docker container to verify contents:
`docker exec -it <name_of_container> /bin/bash`
`docker exec -it ece356_db /bin/bash`