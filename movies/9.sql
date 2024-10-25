SELECT
DISTINCT name
FROM people
WHERE id IN
(
    select person_id
    FROM stars
    WHERE movie_id IN (

        SELECT id
        FROM movies
        WHERE year = 2004
    )
)
ORDER BY
birth;
