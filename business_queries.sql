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
--Limit 7;

/*
Query the database to get the months that produced the most sales
*/
SELECT ROUND( SUM(CAST(dim_products.product_price AS NUMERIC) * orders_table.product_quantity), 2) AS total_sales,
	   dim_date_times.month 
FROM dim_products
INNER JOIN orders_table ON dim_products.product_code = orders_table.product_code
INNER JOIN dim_date_times ON dim_date_times.date_uuid = orders_table.date_uuid
GROUP BY dim_date_times.month
ORDER BY total_sales DESC;

/*
Query the database to get the number of sales
Happening online vs offline Calaucitng the number
of products
sold
*/
WITH online_web_sales as
(
SELECT dim_store_details.store_type,
	   orders_table.product_quantity,
-- A SELCT subquery might allow this to work	   
CASE 
	WHEN dim_store_details.store_type = 'Web Portal' THEN 'Web'
	ELSE 'Offline'
	END AS location
FROM dim_store_details
INNER JOIN orders_table ON dim_store_details.store_code = orders_table.store_code
)

SELECT COUNT(product_quantity) as number_of_sales,
	   sum(product_quantity) as product_quantity_count,	
	   location
FROM online_web_sales
GROUP BY location
ORDER BY number_of_sales ASC;


---  TO DO: FIX the rounding issue.
WITH store_sales as 
(
SELECT
	dim_store_details.store_type,
	SUM(dim_products.product_price * orders_table.product_quantity ) as total_sales
	
FROM dim_products
INNER JOIN orders_table ON dim_products.product_code = orders_table.product_code
INNER JOIN dim_store_details ON dim_store_details.store_code = orders_table.store_code
GROUP BY dim_store_details.store_type
)

SELECT store_type, 
	   ROUND(CAST(total_sales AS NUMERIC), 2),
       total_sales / sum(total_sales) OVER() * 100 as "percentage_total(%)"
FROM store_sales
ORDER BY total_sales DESC;

/*
QUERY Which years produced the highest sales total
*/
SELECT ROUND( SUM(CAST(dim_products.product_price AS NUMERIC) * orders_table.product_quantity), 2) AS total_sales,
	   dim_date_times.year,
	   dim_date_times.month
FROM dim_products
INNER JOIN orders_table ON dim_products.product_code = orders_table.product_code
INNER JOIN dim_date_times ON dim_date_times.date_uuid = orders_table.date_uuid
GROUP BY dim_date_times.year, dim_date_times.month
ORDER BY total_sales DESC;

/*
QUERY to claulate the headcount
*/
SELECT SUM(staff_numbers) as total_staff_numbers,
	   country_code
FROM dim_store_details 
GROUP BY country_code
ORDER BY total_staff_numbers DESC;

/*
QUERY to get the total sales for German store
split by store type. 
*/
WITH GERMAN_stores as
(
SELECT dim_products.product_price,
	   orders_table.product_quantity,
	   dim_store_details.store_type,
	   dim_store_details.country_code
FROM dim_products
INNER JOIN orders_table ON dim_products.product_code = orders_table.product_code
INNER JOIN dim_store_details ON dim_store_details.store_code = orders_table.store_code
WHERE dim_store_details.country_code = 'DE'
)
SELECT ROUND( SUM(CAST(product_price AS NUMERIC) * product_quantity), 2) AS total_sales,
	   store_type,
       country_code
FROM GERMAN_stores
GROUP BY store_type, country_code
ORDER BY total_sales ASC;
/*
SELECT * FROM orders_table
SELECT * FROM dim_card_details
SELECT * FROM dim_date_times
SELECT * FROM dim_products
SELECT * FROM dim_store_details
SELECT * FROM dim_users
*/