SELECT station.name as Station, AVG(`PM2.5`) AS `PM2.5`, AVG(`VPM2.5`) AS `VPM2.5`
FROM reading, station
WHERE reading.station_id = station.id
AND YEAR(reading.`Date Time`) = 2019
AND HOUR(CONVERT_TZ(reading.`Date Time`, 'UTC', 'Europe/London')) = 8
GROUP BY station.name

