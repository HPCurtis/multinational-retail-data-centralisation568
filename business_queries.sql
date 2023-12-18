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

/*
QUERY to get the total sales and their associated sale 
percentage split by store_type 
*/
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
QUERY to calculate the headcount across counrty code
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
Query to get the average time between sales grouped by year
*/
/* ALTER the table and add a timestamp column
then update that column with timestamp.
*/
ALTER TABLE dim_date_times
ADD COLUMN combined_timestamp TIMESTAMP;

UPDATE dim_date_times
SET combined_timestamp = MAKE_DATE(year::int, month::int, day::int) + timestamp::TIME;

/*
Order data into cte to then be average below
*/
with Date_time_ordered as
(
SELECT LEAD(combined_timestamp) OVER(ORDER BY year, combined_timestamp) - combined_timestamp AS lead_time,
	   year,
       combined_timestamp
FROM dim_date_times
),
average as (
-- Get the actual time taken grouped by year
SELECT year,
       AVG(lead_time) as actual_time_taken_1
FROM 
	Date_time_ordered
GROUP BY year
ORDER By actual_time_taken_1 DESC
)

SELECT year,
    TO_JSON(
        json_build_object(
            'hours', (extract(epoch from actual_time_taken_1) / 3600)::int,
            'minutes', ((extract(epoch from actual_time_taken_1) % 3600) / 60)::int,
            'seconds', (extract(epoch from actual_time_taken_1) % 60)::int,
            'milliseconds', (extract(milliseconds from actual_time_taken_1))::int
        )
    ) AS actual_time_taken
FROM average;