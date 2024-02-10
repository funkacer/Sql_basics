-- use weather db from openweathermap;

select t1.w_main_temp as w_temp, from_unixtime(t2.w_dt) as w_dt, "min" as what
from (select min(w_main_temp) as w_main_temp from weather) t1
join weather t2
on t1.w_main_temp = t2.w_main_temp
UNION ALL (
select t1.w_main_temp as w_temp, from_unixtime(t2.w_dt) as w_dt, "max" as what
from (select max(w_main_temp) as w_main_temp from weather) t1
join weather t2
on t1.w_main_temp = t2.w_main_temp);