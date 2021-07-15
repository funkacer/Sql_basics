/****** Script for SelectTopNRows command from SSMS  ******/
SELECT temperature, COUNT(*) AS count
FROM [dbMOJE].[dbo].[condition]
GROUP BY temperature ORDER BY count DESC;