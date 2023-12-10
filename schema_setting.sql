-- ALter the data type of the orders table
ALTER TABLE orders_table
    ALTER COLUMN card_number TYPE VARCHAR,
	ALTER COLUMN store_code TYPE VARCHAR,
	ALTER COLUMN product_code TYPE VARCHAR,
	ALTER COLUMN product_code TYPE VARCHAR,
	/* UUID splveERROR:  column "user_uuid" cannot be cast automatically to type uuid
		HINT:  You might need to specify "USING user_uuid::uuid". 
	*/
	--ALTER COLUMN date_uuid TYPE UUID,
	--ALTER COLUMN user_uuid TYPE UUID,
	ALTER COLUMN product_quantity TYPE SMALLINT;
	
	
	

-- SELECT product_quantity FROM orders_table
	