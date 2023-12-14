-- Alter the data types of the orders table
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

-- Alter the data types of the dim_users
ALTER TABLE dim_users
	ALTER COLUMN first_name
	TYPE VARCHAR(255),
	
	ALTER COLUMN last_name
	TYPE VARCHAR(255),
	
	ALTER COLUMN country_code
	TYPE VARCHAR,
	
	ALTER COLUMN date_of_birth
	TYPE DATE
	USING date_of_birth::DATE,
	
	ALTER COLUMN join_date
	TYPE DATE
	USING join_date::DATE,
	
	ALTER COLUMN user_uuid 
	TYPE UUID
	USING user_uuid::uuid;
	
-- Combine latitude columns columns
ALTER TABLE dim_store_details
	ADD COLUMN Latitude_m TEXT;

UPDATE dim_store_details
set Latitude_m = CONCAT(lat, latitude);

ALTER TABLE dim_store_details
	DROP COLUMN lat,
	DROP COLUMN latitude;
	
ALTER TABLE dim_store_details
	RENAME COLUMN Latitude_m TO latitude;
	

/*
REMOVE NULL values from dim_store_details
table so can be convertedd to float
*/
DELETE FROM dim_store_details 
WHERE longitude = 'N/A';

-- ALter the data types of the dim_store_details
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


-- Alter dim_products table

ALTER TABLE dim_products
	REMOVE £ symbol from prices.
	ALTER COLUMN product_price
	TYPE FLOAT
	USING REPLACE(product_price, '£', '')::float;

ALTER TABLE dim_products
	ADD COLUMN weight_class VARCHAR,
	ALTER COLUMN weight
	TYPE FLOAT
	USING weight::float;

UPDATE dim_products
set weight_class = 'light'
WHERE weight < 2;

UPDATE dim_products
set weight_class = 'Mid_Sized'
WHERE weight >= 2 AND weight < 40;

UPDATE dim_products
set weight_class = 'Heavy'
WHERE weight >= 40 AND weight < 140;

UPDATE dim_products
set weight_class = 'Truck_Required'
WHERE weight >= 140;

-- Rename columns
ALTER TABLE dim_products
	RENAME COLUMN removed TO still_available;

/* 
Convert column to allow for BOOLEAN type below
*/

UPDATE dim_products
set still_available = 0
WHERE still_available = 'Removed';

UPDATE dim_products
set still_available = 1
WHERE still_available = 'Still_avaliable';


ALTER TABLE dim_products
	ALTER COLUMN EAN
	TYPE VARCHAR
	
	ALTER COLUMN still_available
	TYPE BOOLEAN
	USING still_available::boolean,
	
	ALTER COLUMN date_added
	TYPE DATE
	USING date_added::DATE,
	
	ALTER COLUMN uuid 
	TYPE UUID
	USING uuid::uuid,
	
	ALTER COLUMN product_code
	TYPE VARCHAR;

SELECT * FROM dim_products

-- ALter dim_date_times data types.
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


