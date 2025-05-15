-- Top 10 most common genres
SELECT listed_in, COUNT(*) as count
FROM netflix_titles
GROUP BY listed_in
ORDER BY count DESC
LIMIT 10;

-- Number of shows per country
SELECT country, COUNT(*) as count
FROM netflix_titles
GROUP BY country
ORDER BY count DESC
LIMIT 10;

-- Most frequent actors
SELECT cast, COUNT(*) as count
FROM netflix_titles
GROUP BY cast
ORDER BY count DESC
LIMIT 10;

-- Most frequent directors
SELECT director, COUNT(*) as count
FROM netflix_titles
GROUP BY director
ORDER BY count DESC
LIMIT 10;

-- Year-wise content trend
SELECT release_year, COUNT(*) as count
FROM netflix_titles
GROUP BY release_year
ORDER BY release_year;

-- Content type distribution: Movies vs TV Shows
SELECT type, COUNT(*) as count
FROM netflix_titles
GROUP BY type;