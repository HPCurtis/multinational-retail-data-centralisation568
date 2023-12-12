/*
SELECT column_name, data_type
FROM 
	information_schema.columns
WHERE 
	table_name = 'dim_users';
*/

-- ALter the data type of the orders table
ALTER TABLE orders_table
    ALTER COLUMN card_number 
	TYPE VARCHAR,
	
	ALTER COLUMN store_code 
	TYPE VARCHAR,
	
	ALTER COLUMN product_code
	TYPE VARCHAR,

	ALTER COLUMN date_uuid
	TYPE UUID
	USING user_uuid::uuid,
	
	ALTER COLUMN user_uuid 
	TYPE UUID
	USING user_uuid::uuid,
	
	ALTER COLUMN product_quantity 
	TYPE SMALLINT;

ALTER TABLE dim_users
	ALTER COLUMN first_name
	TYPE VARCHAR(255),
	
	ALTER COLUMN last_name
	TYPE VARCHAR(255),
	
	ALTER COLUMN country_code
	TYPE VARCHAR,
	
	-- TO DO check query again and clean up the issues with
	-- Date and UUID conversion. probably in nthe python file
	ALTER COLUMN date_of_birth
	TYPE DATE
	USING date_of_birth::DATE,
	
	ALTER COLUMN join_date
	TYPE DATE
	USING join_date::DATE,
	
	ALTER COLUMN user_uuid 
	TYPE UUID
	USING user_uuid::uuid;

ALTER TABLE dim_store_details
	ALTER COLUMN longitude
	TYPE FLOAT
	USING longitude::double precision,
	
	ALTER COLUMN locality
	TYPE VARCHAR(255),
	
	ALTER COLUMN store_code
	TYPE VARCHAR,
	
	ALTER COLUMN staff_numbers
	TYPE SMALLINT
	USING staff_numbers::smallint,
	
	ALTER COLUMN opening_date
	TYPE DATE
	USING opening_date::DATE,
	
	ALTER COLUMN store_type
	TYPE VARCHAR(255),
	
	ALTER COLUMN latitude
	TYPE FLOAT
	USING longitude::double precision,
	
	ALTER COLUMN country_code
	TYPE VARCHAR,
	
	ALTER COLUMN continent
	TYPE VARCHAR(255);
		
-- ALter dim_store_details data types.
ALTER TABLE dim_date_times
	ALTER COLUMN month
	TYPE VARCHAR,
	
	ALTER COLUMN year
	TYPE VARCHAR,
	
	ALTER COLUMN day
	TYPE VARCHAR,
	
	ALTER COLUMN time_period
	TYPE VARCHAR,
	
	ALTER COLUMN date_uuid 
	TYPE UUID
	USING date_uuid::uuid;
	
ALTER TABLE dim_card_details

-- find out the lenght of these variables
	ALTER COLUMN card_number
	TYPE VARCHAR,
	
	ALTER COLUMN expiry_date
	TYPE VARCHAR,
	
	ALTER COLUMN date_payment_confirmed
	TYPE DATE
	USING date_payment_confirmed::DATE;


UPDATE dim_products
SET product_price = replace(product_price, '£', '')

SELECT product_price FROM dim_products
--SELECT product_price FROM dim_products;
-- SELECT * FROM dim_card_details;