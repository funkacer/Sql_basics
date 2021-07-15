/****** Script for SelectTopNRows command from SSMS  ******/
SELECT DISTINCT 
      [temperature]
  FROM [dbMOJE].[dbo].[condition] ORDER BY temperature ASC;