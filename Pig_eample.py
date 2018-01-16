[10:45 AM, 1/15/2018] +1 (315) 420-2790: ratings = LOAD '/user/maria_dev/ml-100k/u.data' AS (userID:int, movieID:int, rating:int, ratingTime:int);

metadata = LOAD '/user/maria_dev/ml-100k/u.item' USING PigStorage('|')
	AS (movieID:int, movieTitle:chararray, releaseDate:chararray, videoRelease:chararray, imdbLink:chararray);
    
    nameLookup = FOREACH metadata GENERATE movieID, movieTitle,
    ToUnixTime(ToDate(releaseDate, 'dd-MMM-yyyy')) AS releaseTime;
    
    ratingsByMovie = GROUP ratings BY movieID;
    
    avgRatings = FOREACH ratingsByMovie GENERATE group AS movieID, COUNT(ratings.rating) AS avgRating;
    
    oneStarMovies = FILTER avgRatings BY avgRating < 2.0;
    
    oneStarsWithData = JOIN oneStarMovies BY movieID, nameLookup BY movieID;
    
    oldestOneStarMovies = ORDER oneStarsWithData BY nameLookup::releaseTime DESC;
    
    DUMP oldestOneStarMovies;
