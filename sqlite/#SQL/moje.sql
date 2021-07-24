drop table if exists Moje1;
create table Moje1 (id integer primary key autoincrement, value real, code text);
insert into Moje1 (id, value, code) values (Null, 1.0, 'Ahoj 1');
select * from moje1;
insert into Moje1 (id, value, code) values (Null, 2.5, 'Ahoj 2');
select * from moje1;
insert into Moje1 (id, value, code) values (Null, 3, 'Ahoj 3');
select * from moje1;
select round(avg(value), 2) as AVG from Moje1;
select value from moje1 where value > (select round(avg(value), 2) as AVG from Moje1);
with t1 as (select round(avg(value), 2) as average from Moje1)
select * from moje1 where value > (select average from t1);
with t1 as (select round(avg(value), 2) as average from Moje1)
SELECT code, value, id
   FROM moje1
   UNION ALL
SELECT 'Average', average, 0 FROM t1;
with t1 as (select round(avg(value), 2) as average from Moje1)
SELECT code, value, id
   FROM moje1
   UNION ALL
SELECT 'Average', average, Null FROM t1;
