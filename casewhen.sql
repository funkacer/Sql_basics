SELECT text, temperature, CASE
    WHEN temperature > 20 THEN 'The temperature is greater than 20'
    WHEN temperature = 20 THEN 'The temperature is 20'
    ELSE 'The temperature is under 20'
END AS QuantityText
FROM Weather_db_20200118.condition;

SELECT text, temperature, CASE
    WHEN temperature > 20 THEN 'The temperature is greater than 20'
    WHEN temperature >= 0 and temperature <= 20 THEN 'The temperature is 0-20'
    ELSE 'The temperature is under 0'
END AS QuantityText
FROM Weather_db_20200621.condition;

SELECT _id, text, temperature FROM Weather_db_20200621.condition
ORDER BY
(CASE
    WHEN text IS NULL THEN temperature
    ELSE _id
END)
;

SELECT text, temperature, CASE
    WHEN text = "Breezy" THEN temperature
    ELSE Null
END AS t_Breezy, CASE
    WHEN text = "Cloudy" THEN temperature
    ELSE Null
END AS t_Cloudy
FROM Weather_db_20200621.condition;