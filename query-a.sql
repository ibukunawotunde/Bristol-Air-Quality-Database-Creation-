SELECT reading.`Date Time`, station.name, reading.NOX
FROM reading INNER JOIN station ON reading.station_id = station.id WHERE reading.`Date Time` LIKE '2019%' 
ORDER BY reading.NOX DESC LIMIT 1;