/****** Script for SelectTopNRows command from SSMS  ******/
SELECT SUM (A.C1) AS SUMA FROM 
(SELECT COUNT (*) AS C1
  FROM [dbMOJE].[dbo].[20200118_forecast]
  UNION
 SELECT COUNT (*) AS C1
  FROM [dbMOJE].[dbo].[20200621_forecast]) AS A;