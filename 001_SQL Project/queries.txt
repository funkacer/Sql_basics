/*Query 1*/
SELECT f.film_id AS film_id, f.title AS title, c.name AS category, COUNT(i.inventory_id) AS inventory_count
  FROM film AS f
  LEFt JOIN film_category AS fc
    ON f.film_id = fc.film_id
  LEFt JOIN category AS c
    ON fc.category_id = c.category_id
  LEFT JOIN film_actor AS fa
    ON f.film_id = fa.film_id 
  LEFT JOIN actor AS a
    ON fa.actor_id = a.actor_id
  JOIN inventory AS i
    ON i.film_id = f.film_id
 WHERE a.actor_id IS NULL
 GROUP BY 1, 2, 3
 ORDER BY 4 DESC;


/*Query 2*/
WITH t1 AS
(SELECT c.name AS category, SUM(p.amount) AS total_amount, COUNT(r.rental_id) as number_of_rentals
   FROM film AS f
   LEFt JOIN film_category AS fc
     ON f.film_id = fc.film_id
   LEFt JOIN category AS c
     ON fc.category_id = c.category_id
   JOIN inventory AS i
     ON i.film_id = f.film_id
   JOIN rental AS r
     ON i.inventory_id = r.inventory_id
   JOIN payment AS p
    ON p.rental_id = r.rental_id
  GROUP BY 1
  ORDER BY 2 DESC)

(SELECT *
   FROM t1)
  UNION ALL
(SELECT 'TOTAL', SUM(total_amount), SUM(number_of_rentals)
   FROM t1);


/*Query 3*/
SELECT rental_day_of_week, daily_sum_amount,
       SUM(daily_sum_amount) OVER (ORDER BY rental_date) AS cumulative_sum_amount
  FROM (SELECT SUM(p.amount) AS daily_sum_amount, DATE_PART('dow', r.rental_date) AS rental_date,
               CASE DATE_PART('dow', r.rental_date)
               WHEN 0 THEN 'Sunday'
               WHEN 1 THEN 'Monday'
               WHEN 2 THEN 'Tuesday'
               WHEN 3 THEN 'Wednesday'
               WHEN 4 THEN 'Thursday'
               WHEN 5 THEN 'Friday'
               ELSE 'Saturday' END AS rental_day_of_week
          FROM film AS f
          JOIN inventory AS i
            ON i.film_id = f.film_id
          JOIN rental AS r
            ON i.inventory_id = r.inventory_id
          JOIN payment AS p
            ON p.rental_id = r.rental_id
         GROUP BY 2,3 
         ORDER BY 2) t1;


/*Query 4*/
SELECT DATE_PART('year', r.rental_date) AS year,
       DATE_PART('month', r.rental_date) AS month,
       sta.store_id AS store_id, COUNT(r.rental_id) AS rentals_count
  FROM rental r
  JOIN staff sta
    ON r.staff_id = sta.staff_id
 GROUP BY 1, 2, 3
 ORDER BY 4 DESC;