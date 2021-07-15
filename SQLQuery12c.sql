SELECT "text", "creatat", CAST(COUNT(*)* 100.0 / sum(count(*)) over() AS DECIMAL(5,2)) AS "Record_Count"
FROM [dbMOJE].[dbo].[20200118_condition]
WHERE  "creatat" >= CONVERT(DATETIME, N'2020-01-01 00:00:00', 120) AND "creatat" < CONVERT(DATETIME, N'2020-01-02 00:00:00', 120)
GROUP BY "text", "creatat"ORDER BY 2 ASC;

