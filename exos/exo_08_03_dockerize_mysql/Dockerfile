FROM mysql:5.6

# set root password
ENV MYSQL_ROOT_PASSWORD=pass

# create database and table
RUN chown -R mysql:mysql /docker-entrypoint-initdb.d/
COPY init.sql /docker-entrypoint-initdb.d/init.sql


# add a new user
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=user-password

EXPOSE 3306