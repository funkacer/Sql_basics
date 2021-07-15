SELECT "text", "creatat", COUNT(*)* 100.0 / (SELECT count(*) FROM "Weather_db_20200118"."condition"
WHERE "creatat" >= "2020-01-01" and "creatat" < "2020-01-02") AS "Record_count"
FROM "Weather_db_20200118"."condition"
WHERE "creatat" >= "2020-01-01" and "creatat" < "2020-01-02"
GROUP BY "text", "creatat" ORDER BY 2 ASC;
