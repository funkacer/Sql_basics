/****** Script for SelectTopNRows command from SSMS  ******/
SELECT SUM (A.C1) FROM 
(SELECT COUNT (*) AS C1
  FROM [dbMOJE].[dbo].[20200118_condition]
  UNION
 SELECT COUNT (*) AS C1
  FROM [dbMOJE].[dbo].[20200621_condition]) AS A;