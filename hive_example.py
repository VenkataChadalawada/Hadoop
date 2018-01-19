CREATE VIEW topmovieIDs AS
SELECT movieID, count(movieID) as ratingCount
FROM u
GROUP BY movieID
ORDER BY ratingCount DESC;

SELECT n.title, ratingCount
FROM topMovieIDs t JOIN names n ON t.movieID = n.movieID;

# create view if not exist

CREATE VIEW IF NOT EXISTS topmovieIDs AS
SELECT movieID, count(movieID) as ratingCount
FROM u
GROUP BY movieID
ORDER BY ratingCount DESC;

SELECT n.title, ratingCount
FROM topMovieIDs t JOIN names n ON t.movieID = n.movieID;

#TO DELETE A VIEW
DROP VIEW topmovieIDs

#creating table and loading data into hive

CREATE TABLE ratings (
  userID INT,
  movieID INT,
  rating INT,
  time INT)
ROW FORMAT DELIMTIED
FIELDS TERMINATED BY '/t'
STORED AS TEXTFILE;

LOAD DATA LOCAL INPATH '${env:HOME}/ml-100k/u.data'
OVERWRITE INTO TABLE ratings;

#EXTERNAL TABLE VS MANAGED
CREATE EXTERNAL TABLE IF NOT EXISTS ratings (
  userID INT,
  movieID INT,
  rating INT,
  time INT)
ROW FORMAT DELIMTIED
FIELDS TERMINATED BY '/t'

LOCATION '/data/ml-100k/u.data';

#PARTITIONING

- we can store data in partitioned subdirectories

CREATE TABLE customers (
  name STRING,
  address STRUCT <street:STRING,city:STRING,state:STRING,zip:INT>
)
PARTITIONED BY(country STRING);
 
  ---SAVED AS-- ../customers/country=CA/
                ../customers/country=GB/
