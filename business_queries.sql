/*
QUERY to get countires that are operated in 
and the number of stores in each country in
descending order.
*/

SELECT country_code, COUNT(country_code)  
FROM dim_store_details  
GROUP BY country_code
ORDER BY COUNT(country_code) DESC;

/* 
Query to show the locations with the great number of stores.
*/
SELECT locality, COUNT(locality)
FROM dim_store_details
GROUP BY locality
ORDER BY COUNT(locality) DESC;

/*
QUery the database to get the months that produced the most sales
*/