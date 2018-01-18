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
