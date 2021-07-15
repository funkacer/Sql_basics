select
    count(case when text = 'Cloudy' then 1 end) as CLOUDY,
    count(case when text = 'Breezy' then 1 end) as BREEZY
from [dbMOJE].[dbo].[condition];