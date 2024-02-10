-- Active: 1670262542288@@127.0.0.1@8889@parch_and_posey
SHOW TABLES;

DESC accounts;

SHOW CREATE TABLE accounts;

SELECT account_id,
        occurred_at,
        standard_qty,
        gloss_qty,
        poster_qty
FROM orders
WHERE (standard_qty = 0 OR gloss_qty = 0 OR poster_qty = 0)
AND occurred_at >= '2016-10-01';
-- returns 443 rows;

SELECT  account_id,
        total_amt_usd
FROM orders
ORDER BY account_id, total_amt_usd DESC
LIMIT 30;
-- první je automaticky ASC;

SELECT id, account_id, total_amt_usd
FROM orders
WHERE total_amt_usd = 0
ORDER BY total_amt_usd DESC, account_id;
-- returns 2O rows;

SELECT name, website, primary_poc
FROM accounts
WHERE name = 'Exxon Mobil';
-- 1 row;

SELECT id, account_id, poster_amt_usd/(standard_amt_usd+gloss_amt_usd +poster_amt_usd) AS poster_usd_perc
FROM orders
WHERE (standard_amt_usd+gloss_amt_usd +poster_amt_usd) = 0;
-- returns null on 20 rows;

SELECT *
FROM accounts
WHERE website LIKE '%google%';
-- any number of characters;

SELECT name FROM accounts
WHERE name LIKE '%s';
-- returns 81 results opposite to 77 in POSTGRE - incl S;

SET @s = BINARY '%S';
SELECT name FROM accounts
WHERE name LIKE @s;
-- this is case sensitive;

SELECT *
FROM orders
WHERE account_id IN (1001,1021);
-- 38 rows;

SELECT *
FROM accounts
WHERE website NOT LIKE '%com%';
-- 2 rows;

SELECT SUM(count) from (SELECT channel, count(*) as count
FROM web_events
WHERE channel NOT IN ('organic', 'adwords')
GROUP BY 1) t1;
-- is 7214, should be 7215 - caused by id 4831;

SET @row_number = 0; 

SELECT * FROM (SELECT (@row_number:=@row_number + 1) AS num, id
FROM web_events) t1
WHERE num != id;
-- odhalilo chybějící 4831;

SELECT * FROM web_events WHERE id = 4831;
-- zde bylo špatné datum (mezi 2-3 ráno není kvůli DST);

SELECT o.*, a.*
FROM orders o
JOIN accounts a
ON o.account_id = a.id;
-- 6912;

SELECT r.name region, s.name rep, a.name account
FROM sales_reps s
JOIN region r
ON s.region_id = r.id
JOIN accounts a
ON a.sales_rep_id = s.id
ORDER BY a.name;
-- 351;

SELECT orders.*, accounts.*
FROM orders
LEFT JOIN accounts
ON orders.account_id = accounts.id 
AND accounts.sales_rep_id = 321500;
--prefilters second table, but shows all orders;

SELECT r.name r_name, s.name s_name, a.name a_name
FROM sales_reps s
JOIN region r
ON s.region_id = r.id
AND r.name = 'Midwest'
AND s.name LIKE 'S%'
JOIN accounts a
ON s.id = a.sales_rep_id
ORDER BY a.name;
--  5;

SELECT o.occurred_at, a.name, o.total, o.total_amt_usd
FROM accounts a
JOIN orders o
ON o.account_id = a.id
WHERE o.occurred_at BETWEEN '2015-01-01' AND '2016-01-01'
ORDER BY o.occurred_at DESC;
-- 1725;

