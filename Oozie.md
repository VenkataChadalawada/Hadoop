# Oozie
#### A system for running and scheduling hadoop tasks.
- might chain together MapReduce, Hive, Pig, Sqoop and dist cp tasks
- other systems available via add-ons (like spark)
- workflow is a Directed Acyclic Graph of actions
- specified via XML
- so, you can run actions that don't depend on each other in parallel

#### Types of difff things in OOzie
forks
coordinatenodes
groups
bundles

#### Opening MySQL
mysql -u root -p
hadoop

#### exit & download the script
source movielens.sql

#### show data bases
show databases;
set names 'utf8';
set character set utf8;
create database movielens;
use movielens;
create database movielens;
use movielens;
#### exit & download a script that creates a users table
wget http://media.sundog-soft.com/hadoop/movielens.sql
[root@sandbox-hdp bin]# vi movielens.sql 
``` sql
BEGIN;

DROP TABLE IF EXISTS occupations;
CREATE TABLE occupations (
  id integer NOT NULL,
  name varchar(255),
  PRIMARY KEY (id)
);
INSERT INTO occupations VALUES (1,'Administrator'),(2,'Artist'),(3,'Doctor'),(4,'Educator'),(5,'Engineer'),(6,'Entertainment'),(7,'Executive'),(8,'Healthcare'),(9,'Homemaker'),(10,'Lawyer'),(11,'Librarian'),(12,'Marketing'),(13,'None'),(14,'Other'),(15,'Programmer'),(16,'Retired'),(17,'Salesman'),(18,'Scientist'),(19,'Student'),(20,'Technician'),(21,'Writer');

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id integer NOT NULL,
  age integer,
  gender char(1),
  occupation_id integer,
  zip_code varchar(255),
  PRIMARY KEY (id)
);
INSERT INTO users VALUES (1,24,'M',20,'85711'),(2,53,'F',14,'94043'),(3,23,'M',21,'32067'),(4,24,'M',20,'43537'),(5,33,'F',14,'15213'),(6,42,'M',7,'98101'),(7,57,'M',1,'91344'),(8,36,'M',1,'05201'),(9,29,'M',19,'01002'),(10,53,'M',10,'90703'),(11,39,'F',14,'30329'),(12,28,'F',14,'06405'),(13,47,'M',4,'29206'),(14,45,'M',18,'55106'),(15,49,'F',4,'97301'),(16,21,'M',6,'10309'),(17,30,'M',15,'06355'),(18,35,'F',14,'37212'),(19,40,'M',11,'02138'),(20,42,'F',9,'95660'),(21,26,'M',21,'30068'),(22,25,'M',21,'40206'),(23,30,'F',2,'48197'),(24,21,'F',2,'94533'),(25,39,'M',5,'55107'),(26,49,'M',5,'21044'),(27,40,'F',11,'30030'),(28,32,'M',21,'55369'),(29,41,'M',15,'94043'),(30,7,'M',19,'55436'),(31,24,'M',2,'10003'),(32,28,'F',19,'78741'),(33,23,'M',19,'27510'),(34,38,'F',1,'42141'),(35,20,'F',9,'42459'),(36,19,'F',19,'93117'),(37,23,'M',19,'55105')

DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings (
  id integer NOT NULL,
  user_id integer,
  movie_id integer,
  rating integer,
  rated_at timestamp,
  PRIMARY KEY (id)
);
INSERT INTO ratings VALUES (1,196,242,3,'1997-12-04 07:55:49'),(2,186,302,3,'1998-04-04 11:22:22'),(3,22,377,1,'1997-11-06 23:18:36'),(4,244,51,2,'1997-11-26 21:02:03'),(5,166,346,1,'1998-02-01 21:33:16'),(6,298,474,4,'1998-01-07 06:20:06'),(7,115,265,2,'1997-12-03 09:51:28'),(8,253,465,5,'1998-04-03 10:34:27'),(9,305,451,3,'1998-02-01 01:20:17'),(10,6,86,3,'1997-12-31 13:16:53'),(11,62,257,2,'1997-11-12 14:07:14'),(12,286,1014,5,'1997-11-17 07:38:45'),(13,200,222,5,'1997-10-05 02:05:40'),(14,210,40,3,'1998-03-27 13:59:54'),(15,224,29,3,'1998-02-21 15:40:57'),(16,303,785,3,'1997-11-13 21:28:38'),(17,122,387,5,'1997-11-11 09:47:39'),(18,194,274,2,'1997-11-14 12:36:34'),(19,291,1042,4,'1997-09-21 02:42:24'),(20,234,1184,2,'1998-04-08 16:47:17'),(21,119,392,4,'1998-01-30 08:13:34'),(22,167,486,4,'1998-04-16 07:54:12'),(23,299,144,4,'1997-10-26 07:55:20'),(24,291,118,2,'1997-09-21 02:24:38'),(25,308,1,4,'1998-02-17 09:28:52'),(26,95,546,2,'1997-11-10 13:16:06'),(27,38,95,5,'1998-04-12 18:14:54'),(28,102,768,2,'1998-01-02 05:40:50'),(29,63,277,4,'1997-10-01 16:10:01'),(30,160,234,5,'1997-10-14 13:33:05'),(31,50,246,3,'1997-10-16 18:38:49'),(32,301,98,4,'1997-12-13 21:03:47'),(33,225,193,4,'1997-11-14 12:35:27'),(34,290,88,4,'1997-11-28 07:46:03'),(35,97,194,3,'1998-01-07 21:54:20'),(36,157,274,4,'1998-02-07 14:33:55'),(37,181,1081,1,'1997-11-07 20:17:03'),(38,278,603,5,'1998-03-30 14:02:10'),(39,276,796,1,'1997-09-20 14:45:32'),(40,7,32,4,'1998-03-31 05:28:52'),(41,10,16,4,'1997-10-26 10:01:17'),(42,284,304,4,'1998-01-20 12:48:42'),(43,201,979,2,'1998-01-06 11:17:13'),(44,276,564,3,'1997-09-20 14:43:25'),(45,287,327,5,'1997-09-26 21:18:36'),(46,246,201,5,'1998-01-15 19:33:14'),(47,242,1137,5,'1997-11-16 20:33:16'),(48,249,241,5,'1997-11-15 16:46:34'),(49,99,4,5,'1998-02-03 07:18:17'),(50,178,332,3,'1997-12-22 12:43:57'),(51,251,100,4,'1998-01-31 10:38:04'),(52,81,432,2,'1997-10-10 18:58:51'),(53,260,322,4,'1998-03-22 18:08:18'),(54,25,181,5,'1998-01-26 14:23:35'),(55,59,196,5,'1998-02-22 19:38:08'),(56,72,679,2,'1997-11-20 06:46:04'),(57,87,384,4,'1997-11-18 10:18:47'),(58,290,143,5,'1997-11-25 08:11:33'),(59,42,423,5,'1997-12-02 16:08:07'),(60,292,515,4,'1997-12-02 15:06:17'),(61,115,20,3,'1997-12-03 09:43:29'),(62,20,288,1,'1997-11-16 00:06:24'),(63,201,219,4,'1998-01-06 10:51:13'),(64,13,526,3,'1997-12-14 15:10:53'),(65,246,919,4,'1998-01-15 19:22:29'),(66,138,26,5,'1997-11-08 13:23:52'),(67,167,232,1,'1998-04-16 07:52:21'),(68,60,427,5,'1997-12-28 08:30:20'),(69,57,304,5,'1998-01-01 15:49:41'),(70,223,274,4,'1998-04-02 12:48:14'),(71,189,512,4,'1998-04-22 13:41:42'),(72,243,15,3,'1997-11-19 16:57:20'),(73,92,1049,1,'1998-03-18 12:10:26'),(74,246,416,3,'1998-01-15 19:57:27'),(75,194,165,4,'1997-11-14 14:32:03'),(76,241,690,2,'1998-02-11 18:11:22'),(77,178,248,4,'1997-12-22 12:52:34'),(78,254,1444,3,'1998-02-02 19:12:38'),(79,293,5,3,'1998-03-02 22:29:36'),(80,127,229,5,'1998-01-09 08:54:27'),(81,225,237,5,'1997-11-14 12:34:03'),(82,299,229,3,'1997-10-29 22:20:29'),(83,225,480,5,'1997-11-14 12:52:28'),(84,276,54,3,'1997-09-20 14:30:25'),(85,291,144,5,'1997-09-21 02:44:51'),(86,222,366,4,'1997-10-29 19:49:41'),(87,267,518,5,'1997-11-07 22:49:33'),(88,42,403,3,'1997-12-02 16:24:44'),
DROP TABLE IF EXISTS movies;
CREATE TABLE movies (
  id integer NOT NULL,
  title varchar(255),
  release_date date,
  PRIMARY KEY (id)
);
INSERT INTO movies VALUES (1,'Toy Story (1995)','1995-01-01'),(2,'GoldenEye (1995)','1995-01-01'),(3,'Four Rooms (1995)','1995-01-01'),(4,'Get Shorty (1995)','1995-01-01'),(5,'Copycat (1995)','1995-01-01'),(6,'Shanghai Triad (Yao a yao yao dao waipo qiao) (1995)','1995-01-01'),(7,'Twelve Monkeys (1995)','1995-01-01'),(8,'Babe (1995)','1995-01-01'),(9,'Dead Man Walking (1995)','1995-01-01'),(10,'Richard III (1995)','1996-01-22'),(11,'Seven (Se7en) (1995)','1995-01-01'),(12,'Usual Suspects, The (1995)','1995-08-14'),(13,'Mighty Aphrodite (1995)','1995-10-30'),(14,'Postino, Il (1994)','1994-01-01'),(15,'Mr. Holland''s Opus (1995)','1996-01-29'),(16,'French Twist (Gazon maudit) (1995)','1995-01-01'),(17,'From Dusk Till Dawn (1996)','1996-02-05'),(18,'White Balloon, The (1995)','1995-01-01'),(19,'Antonia''s Line (1995)','1995-01-01'),(20,'Angels and Insects (1995)','1995-01-01'),(21,'Muppet Treasure Island (1996)','1996-02-16'),(22,'Braveheart (1995)','1996-02-16'),(23,'Taxi Driver (1976)','1996-02-16'),(24,'Rumble in the Bronx (1995)','1996-02-23'),(25,'Birdcage, The (1996)','1996-03-08'),(26,'Brothers McMullen, The (1995)','1995-01-01'),(27,'Bad Boys (1995)','1995-01-01'),(28,'Apollo 13 (1995)','1995-01-01'),(29,'Batman Forever (1995)','1995-01-01'),(30,'Belle de jour (1967)','1967-01-01'),(31,'Crimson Tide (1995)','1995-01-01'),(32,'Crumb (1994)','1994-01-01'),(33,'Desperado (1995)','1995-01-01'),(34,'Doom Generation, The (1995)','1995-01-01'),(35,'Free Willy 2: The Adventure Home (1995)','1995-01-01'),(36,'Mad Love (1995)','1995-01-01'),(37,'Nadja (1994)','1994-01-01'),(38,'Net, The (1995)','1995-01-01'),(39,'Strange Days (1995)','1995-01-01'),(40,'To Wong Foo, Thanks for Everything! Julie Newmar (1995)','1995-01-01'),(41,'Billy Madison (1995)','1995-01-01'),(42,'Clerks (1994)','1994-01-01'),(43,'Disclosure (1994)','1994-01-01')
DROP TABLE IF EXISTS genres;
CREATE TABLE genres (
  id integer NOT NULL,
  name varchar(255),
  PRIMARY KEY (id)
);
INSERT INTO genres VALUES (1,'Action'),(2,'Adventure'),(3,'Animation'),(4,'Children''s'),(5,'Comedy'),(6,'Crime'),(7,'Documentary'),(8,'Drama'),(9,'Fantasy'),(10,'Film-Noir'),(11,'Horror'),(12,'Musical'),(13,'Mystery'),(14,'Romance'),(15,'Sci-Fi'),(16,'Thriller'),(17,'War'),(18,'Western');

DROP TABLE IF EXISTS genres_movies;
CREATE TABLE genres_movies (
  id integer NOT NULL,
  movie_id integer,
  genre_id integer,
  PRIMARY KEY (id)
);
INSERT INTO genres_movies VALUES (1,1,3),(2,1,4),(3,1,5),(4,2,1),(5,2,2),(6,2,16),(7,3,16),(8,4,1),(9,4,5),(10,4,8),(11,5,6),(12,5,8),(13,5,16),(14,6,8),(15,7,8),(16,7,15),(17,8,4),(18,8,5),(19,8,8),(20,9,8),(21,10,8),(22,10,17),(23,11,6),(24,11,16),(25,12,6),(26,12,16),(27,13,5),(28,14,8),(29,14,14),(30,15,8),(31,16,5),(32,16,14),(33,17,1),(34,17,5),(35,17,6),(36,17,11),(37,17,16),(38,18,8),(39,19,8),(40,20,8),(41,20,14),(42,21,1),(43,21,2),(44,21,5),(45,21,12),(46,21,16),(47,22,1),(48,22,8),(49,22,17),(50,23,8),(51,23,16),(52,24,1),(53,24,2),(54,24,6),(55,25,5),(56,26,5),(57,27,1),(58,28,1),(59,28,8),(60,28,16),(61,29,1),(62,29,2),(63,29,5),(64,29,6),(65,30,8),(66,31,8),(67,31,16),(68,31,17),(69,32,7),(70,33,1),(71,33,14),(72,33,16),(73,34,5),(74,34,8),(75,35,2),(76,35,4),(77,35,8),(78,36,8),(79,36,14),(80,37,8),(81,38,15),(82,38,16),(83,39,1),(84,39,6),(85,39,15),(86,40,5),(87,41,5),(88,42,5),(89,43,8),(90,43,16),(91,44,8),(92,44,16),(93,45,5),(94,45,8),(95,46,8),(96,47,5),(97,47,8),(98,48,7),(99,49,5),(100,49,14),(101,50,1),(102,50,2),(103,50,14),(104,50,15),(105,50,17),(106,51,8),(107,51,14),(108,51,17),(109,51,18),(110,52,8),(111,53,1),(112,53,16),(113,54,1),(114,54,8),(115,54,16),(116,55,6),(117,55,8),(118,55,14),(119,55,16),(120,56,6),(121,56,8),(122,57,8),(123,58,8),(124,59,8),(125,60,8),(126,61,8),(127,62,1),(128,62,2),(129,62,15),(130,63,4),(131,63,5),(132,64,8),(133,65,5),(134,65,8),(135,66,5),(136,66,14),(137,67,5),(138,68,1),(139,68,14),(140,68,16),(141,69,5),(142,69,14),(143,69,17),(144,70,5),(145,70,14),(146,71,3),(147,71,4),(148,71,12),(149,72,5),(150,72,6),(151,72,9),(152,73,1),(153,73,5),(154,73,18),(155,74,1),(156,74,5),(157,74,8),(158,75,7),(159,76,6),(160,76,8),(161,77,8),(162,77,16),(163,78,2),(164,78,4),(165,78,8),(166,79,1),(167,79,16),(168,80,1),(169,80,5),(170,80,17),(171,81,5),(172,81,14),(173,82,1),(174,82,2),(175,82,15),(176,83,5),(177,83,14),(178,84,11),(179,84,15),(180,85,5),(181,86,8),(182,87,8),(183,88,5),(184,88,14),(185,89,10),(186,89,15),(187,90,5),(188,90,14),(189,90,16),(190,91,4),(191,91,5),(192,91,12),(193,92,1),(194,92,6),(195,92,14),(196,93,5),(197,93,8)
COMMIT;
```     

#### Go to mysql & execute the script
mysql -u root -p
hadoop
use movielens;
source movielens.sql
show tables;
mysql> select * from users limit 10;
+----+------+--------+---------------+----------+
| id | age  | gender | occupation_id | zip_code |
+----+------+--------+---------------+----------+
|  1 |   24 | M      |            20 | 85711    |
|  2 |   53 | F      |            14 | 94043    |
|  3 |   23 | M      |            21 | 32067    |
|  4 |   24 | M      |            20 | 43537    |
|  5 |   33 | F      |            14 | 15213    |
|  6 |   42 | M      |             7 | 98101    |
|  7 |   57 | M      |             1 | 91344    |
|  8 |   36 | M      |             1 | 05201    |
|  9 |   29 | M      |            19 | 01002    |
| 10 |   53 | M      |            10 | 90703    |
+----+------+--------+---------------+----------+
10 rows in set (0.00 sec)
// Now to allow sqoop to access tables
mysql> grant all privileges on movielens.* to ''@'localhost';

#### Exit & download hive script
exit

wget http://media.sundog-soft.com/hadoop/oldmovies.sql

[root@sandbox-hdp bin]# vi oldmovies.sql 

DROP TABLE movies;
CREATE EXTERNAL TABLE movies (movie_id INT, title STRING, release DATE) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' LOCATION '/user/maria_dev/movies/';
INSERT OVERWRITE DIRECTORY '${OUTPUT}' SELECT * FROM movies WHERE release < '1940-01-01' ORDER BY release;

#### download oozie workflow xml
wget http://media.sundog-soft.com/hadoop/workflow.xml
vi workflow.xml
``` xml
<?xml version="1.0" encoding="UTF-8"?>
<workflow-app xmlns="uri:oozie:workflow:0.2" name="old-movies">
    <start to="sqoop-node"/>

    <action name="sqoop-node">
        <sqoop xmlns="uri:oozie:sqoop-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <prepare>
                <delete path="${nameNode}/user/maria_dev/movies"/>
            </prepare>

            <configuration>
                <property>
                    <name>mapred.job.queue.name</name>
                    <value>${queueName}</value>
                </property>
            </configuration>
            <command>import --connect jdbc:mysql://localhost/movielens --driver com.mysql.jdbc.Driver --table movies -m 1</command>
        </sqoop>
        <ok to="hive-node"/>
        <error to="fail"/>
    </action>
    <action name="hive-node">
        <hive xmlns="uri:oozie:hive-action:0.2">
            <job-tracker>${jobTracker}</job-tracker>
            <name-node>${nameNode}</name-node>
            <prepare>
                <delete path="${nameNode}/user/maria_dev/oldmovies"/>
            </prepare>
            <configuration>
                <property>
                    <name>mapred.job.queue.name</name>
                    <value>${queueName}</value>
                </property>
            </configuration>
            <script>oldmovies.sql</script>
            <param>OUTPUT=/user/maria_dev/oldmovies</param>
        </hive>
        <ok to="end"/>
        <error to="fail"/>
    </action>
    <kill name="fail">
        <message>Sqoop failed, error message[${wf:errorMessage(wf:lastErrorNode())}]</message>
    </kill>
    <end name="end"/>
</workflow-app>
```


