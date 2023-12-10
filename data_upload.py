from database_utils import DatabaseConnector 
from data_cleaning  import DataCleaning

pw = '13,Running1'

# Upload pandas dataframes to SQL database 

# Upload order table
#table_list = DatabaseConnector().list_db_tables()

# Upload the orders data.
DatabaseConnector().upload_to_db(df = DataCleaning().clean_orders_data(), 
                                table_name = 'orders_table', password = pw)

# Upload the user data.
DatabaseConnector().upload_to_db(df = DataCleaning().clean_user_data(), 
                                 table_name = 'dim_users', password = pw)

# Upload the events data.
DatabaseConnector().upload_to_db(df = DataCleaning().clean_events_data(), 
                                 table_name = 'dim_date_times', password = pw)

# Upload the products data.
DatabaseConnector().upload_to_db(df = DataCleaning().clean_products_data(), 
                                 table_name = 'dim_products', password = pw)

DatabaseConnector().upload_to_db(df = DataCleaning().clean_store_data(), 
                                 table_name = 'dim_store_details', password = pw)

