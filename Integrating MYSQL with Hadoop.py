 - popular free relational database 
 - Generally monolithic in nature
 - But, can be used for OLTP - so exporting data into MYSQL can be useful
 - Existing data may exist in MYSQL that you want to import to Hadoop to execute more complex queries --- THIS CAN BE DONE BY SQOOP ---
 
 
 SQOOP (SQL + HADOOP)
 It can handle large datasets and import/export them to Hadoop
 It kicks off Mapreduce job to handle import/export of data
 
 
 SQOOP: IMPORT DATA FROM MYSQL TO HDFS
 # this command sucks out movies from mysql table and copies it on hdfs cluster
 
 sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1
 
 #INCREMENTAL IMPORTS
 
 --we can keep our relational databsase and Hadoop in sync
 -- --check-coloum and --last-value
 
 SQOOP: EXPORT DATA FROM HIVE TO MYSQL
 # this command sucks out movies from mysql table and copies it on hdfs cluster
 
 sqoop export --connect jdbc:mysql://localhost/movielens -m 1 --driver
 com.mysql.jdbc.Driver --table exported_movies --export-dir
 /apps/hive/warehouse/movies --input-fields-terminated-by '\0001'
 (target table must already exist in MYSQL,with columns in expected order)
 
# Sqoop data into mysql from hadoop
ssh maria_dev@127.0.0.1 -p2222
# Access mysql as root 
mysql -u root -p ha**
#create database
create database movielens;
#show data bases
show databases;
#getting a file from other website sources into our account
wget http://media.sundog-soft.com/hadoop/movielens.sql
 # view filesystem
 ls (linux / unix/ mac)
 dir (windows)
 #to see any file
 nano movielens.sql
 vi movielens.sql
 less movielens.sql
 # now go back to mysql to execute the downloaded sql
 #set charecter set utf8
  SET NAMES 'utf8';
  SET CHARACTER SET utf8;
# to enter into the database
use movielens;
#running the script downloaded in mysql
source movielens.sql;
#show tables now in this database
show tables;
# view 10 records in any table
select * from movies limit 10;
# to look into metadata of a table
describe movies;
# view data with an example query
SELECT movies.title, AVG(ratings.movie_id) AS ratingAvg FROM movies INNER JOIN ratings ON movies.id = ratings.movie_id GROUP BY movies.title ORDER BY ratingAvg;
#to grant permissions for sqoop to read movielens database
GRANT ALL PRIVILEGES ON movielens.* to ''@'localhost';

# IMPORTING
#bringing a (movies table) table from movielens database using sqoop into hdfs
 sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1
#bringing a (movies table) table from movielens database using sqoop into hive
sqoop import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table occupations -m 1 --hive-import
#now one can see this data inside ambari hive under defaults we can see our occupations table
#Basically at the end hive also stores data in HDFS it just shows users like tables by having some metastore however it relies on hdfs inside  apps > hive > warehouse

#EXPORTING
#lets first create a table in mysql to export the data from hdfs / hive
 mysql -u root -p
 hadoop
 use movielens;
 CREATE TABLE exported_movies (id INTEGER, title VARCHAR(255), releaseData DATE);
 
#now export from hdfs into mysql
sqoop export --connect jdbc:mysql://localhost/movielens -m 1 --driver com.mysql.jdbc.Driver --table exported_occupations --export-dir /apps/hive/warehouse/occupations --inputs-fields-terminated-by '\0001'
