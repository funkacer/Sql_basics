/****** Script for SelectTopNRows command from SSMS  ******/
SELECT COUNT (*) AS C1
  FROM [dbMOJE].[dbo].[20200118_condition]
  UNION
 SELECT COUNT (*) AS C1
  FROM [dbMOJE].[dbo].[20200621_condition];