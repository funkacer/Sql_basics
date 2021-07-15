SELECT * INTO [dbMOJE].[dbo].[condition] FROM (SELECT * FROM [dbMOJE].[dbo].[20200118_condition]
UNION
SELECT * FROM [dbMOJE].[dbo].[20200621_condition]) AS A;