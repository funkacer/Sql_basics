SELECT [text], CAST(COUNT(*)* 100.0 / sum(count(*)) over() AS DECIMAL(5,2)) AS "Record_Count"
FROM [dbMOJE].[cursor].[20200118_condition]
WHERE CAST([creatat] AS DATETIME) >= CONVERT(DATETIME, N'2020-01-01 00:00:00', 120) and CAST([creatat] AS DATETIME) < CONVERT(DATETIME, N'2020-01-02 00:00:00', 120)
GROUP BY [text]
ORDER BY 2 ASC;

