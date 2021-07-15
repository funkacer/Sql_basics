SELECT * INTO [dbMOJE].[dbo].[forecast] FROM (SELECT * FROM [dbMOJE].[dbo].[20200118_forecast]
UNION
SELECT * FROM [dbMOJE].[dbo].[20200621_forecast]) AS A;