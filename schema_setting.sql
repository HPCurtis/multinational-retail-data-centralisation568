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
	USING date_uuid::uuid,
	
	ALTER COLUMN user_uuid 
	TYPE UUID
	USING user_uuid::uuid,
	
	ALTER COLUMN product_quantity 
	TYPE SMALLINT;


-- Alter the data types of the dim_users table
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

/*
Combine latitude columns. Yo achieve this new column
is added and then combined lat and latituue columnsms are Updated t
latitude_m colmn, then the original colms are droped 
and latitude_m renamed to latitude.
*/

ALTER TABLE dim_store_details
	ADD COLUMN Latitude_m TEXT;

UPDATE dim_store_details
set Latitude_m = CONCAT(lat, latitude);

update dim_store_details
set latitude_m = ''
WHERE latitude_m = 'NULLNULL';

-- DROP cloumns
ALTER TABLE dim_store_details
	DROP COLUMN lat,
	DROP COLUMN latitude;
	
-- RENMS ERCOLUMNS	
ALTER TABLE dim_store_details
	RENAME COLUMN Latitude_m TO latitude;


DELETE FROM dim_store_details
WHERE longitude = 'NULL';

-- Convert N/A's to null so the columns can be converted
-- in Longitude and latitude.
update dim_store_details
set longitude = NULL
WHERE longitude = 'N/A';

update dim_store_details
set latitude = NULL
WHERE latitude = 'N/A';

-- ALter the data types of the dim_store_details table
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
	TYPE character varying(255),
	
	ALTER COLUMN latitude
	TYPE FLOAT
	USING latitude::double precision,
	
	ALTER COLUMN country_code
	TYPE VARCHAR,
	
	ALTER COLUMN continent
	TYPE VARCHAR(255);

-- Make store_type NULLABLE
ALTER TABLE dim_store_details
	ALTER COLUMN store_type
	DROP NOT NULL;


-- Alter dim_products table
ALTER TABLE dim_products
	--REMOVE £ symbol from prices.
	ALTER COLUMN product_price
	TYPE FLOAT
	USING REPLACE(product_price, '£', '')::float;

/*Add human readable specification to dim_products
table*/

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

-- Rename removed column
ALTER TABLE dim_products
	RENAME COLUMN removed TO still_available;

/* 
Convert Still_availble column valies
to allow for BOOLEAN type  conversion
below
*/
UPDATE dim_products
set still_available = 0
WHERE still_available = 'Removed';

UPDATE dim_products
set still_available = 1
WHERE still_available = 'Still_avaliable';

/*
Alter the dim_products data types.
*/ 
ALTER TABLE dim_products
	ALTER COLUMN ean
	TYPE VARCHAR,
	
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

-- ALter dim_card_details_times data types.	
ALTER TABLE dim_card_details

	ALTER COLUMN card_number
	TYPE VARCHAR,
	
	ALTER COLUMN expiry_date
	TYPE VARCHAR,
	
	ALTER COLUMN date_payment_confirmed
	TYPE DATE
	USING date_payment_confirmed::DATE;

-- Set the Primary Key for each dim_card_details
ALTER TABLE dim_card_details 
ADD PRIMARY KEY (card_number);

-- Set the Primary Key for dim_date_times
ALTER TABLE dim_date_times 
ADD PRIMARY KEY (date_uuid);

-- Set the Primary Key for dim_products
ALTER TABLE dim_products 
ADD PRIMARY KEY (product_code);

-- Set the Primary Key for dim_store_details
ALTER TABLE dim_store_details 
ADD PRIMARY KEY (store_code);

-- Set the Primary Key for dim_users
ALTER TABLE dim_users 
ADD PRIMARY KEY (user_uuid);

-- Set the foreign keys for data tables 


ALTER TABLE orders_table
	ADD CONSTRAINT fk_date_uuid FOREIGN KEY (date_uuid)
	REFERENCES dim_date_times (date_uuid);


ALTER TABLE orders_table
	ADD CONSTRAINT fk_user_uuid FOREIGN KEY (user_uuid)
	REFERENCES dim_users (user_uuid);

ALTER TABLE orders_table
	ADD CONSTRAINT fk_product_code FOREIGN KEY (product_code)
	REFERENCES dim_products (product_code);
	
ALTER TABLE orders_table
	ADD CONSTRAINT fk_card_details FOREIGN KEY (card_number)
	REFERENCES dim_card_details (card_number);	

ALTER TABLE orders_table
	ADD CONSTRAINT fk_store_code FOREIGN KEY (store_code)
	REFERENCES dim_store_details (store_code);
