-- use weather db from openweathermap;

select date(from_unixtime(w_dt)), avg(w_main_temp) OVER (PARTITION BY date(from_unixtime(w_dt)) ORDER BY date(from_unixtime(w_dt)) ) from weather GROUP BY 1;

--jine vysledky nez
select date(from_unixtime(w_dt)), avg(w_main_temp)  from weather GROUP BY 1;

--stejne jako
select distinct date(from_unixtime(w_dt)), avg(w_main_temp) OVER (PARTITION BY date(from_unixtime(w_dt)) ORDER BY date(from_unixtime(w_dt)) ),
sum(w_main_temp) OVER () from weather ;

--running sum
with t1 AS (select distinct date(from_unixtime(w_dt)) as dt, avg(w_main_temp) OVER (PARTITION BY date(from_unixtime(w_dt)) ORDER BY date(from_unixtime(w_dt)) ) as aver from weather )
select dt, aver, sum(aver) over(ORDER BY dt) from t1;

--running avg
with t1 AS (select distinct date(from_unixtime(w_dt)) as dt, avg(w_main_temp) OVER (PARTITION BY date(from_unixtime(w_dt)) ORDER BY date(from_unixtime(w_dt)) ) as aver from weather )
select dt, aver, avg(aver) over(ORDER BY dt) from t1;

--jak udělat průměrnou teplotu postupně ze všech měření
select distinct date(from_unixtime(w_dt)), avg(w_main_temp) OVER (PARTITION BY date(from_unixtime(w_dt)) ORDER BY date(from_unixtime(w_dt)) ), avg(w_main_temp) OVER (ORDER BY date(from_unixtime(w_dt))) from weather;

--jak ověřit že to funguje?
select avg(w_main_temp) from weather;