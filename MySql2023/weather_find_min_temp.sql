-- use weather db from openweathermap;

select t1.w_main_temp, t2.*, from_unixtime(t2.w_dt)
from (select min(w_main_temp) as w_main_temp from weather) t1
join weather t2
on t2.w_main_temp = t1.w_main_temp;