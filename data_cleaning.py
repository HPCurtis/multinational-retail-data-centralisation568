#!/bin/bash

from database_utils import DatabaseConnector
from data_extraction import DataExtractor

filename = 'db_creds.yaml'

class DataCleaning:

    def df_import(self, tablename):
        # Get dataframe using other methods
        de = DataExtractor()
        table_names = DatabaseConnector(filename = filename).list_db_tables()
        user_table = table_names.index(tablename)

        # Return dataframe
        return(de.read_rds_table(table_names[user_table]))
        

    def clean_user_data(self):
       # Import data 
       df = DataExtractor().read_rds_table('legacy_users')
       # Clean the data

       # Clean data
       return(clean_df)
    
        # Clean user data


    def clean_card_data(self):
        
        #Import card data for cleaning.
        df = DataExtractor().retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')

        # TO DO creat method too  clean the data to remove any erroneous values, NULL values or errors with formatting.
        # Once cleaned, upload the table with your upload_to_db method to the database in a table called dim_card_details. 
        return(df)
    
    def clean_store_data(self):
        #Import store data
        df = DataExtractor().retrieve_stores_data(n_stores = DataExtractor().list_number_of_stores())
        
        # CLean store data.

        return(df)
    
    def clean_products_data(self):
        df = convert_product_weights
        return(0)
    
    def clean_orders_data(self):
        # Import data fraem for cleaning.
        df = DataExtractor().read_rds_table('orders_table')

        # Clean data
        # Drop the first name, last name and 1 columns from dataframe
        df_clean = df.drop(['first_name', 'last_name', '1'],  axis=1)

        # return cleaned dataframe.
        return(df_clean)
    
    def convert_product_weights(self, df = DataExtractor().extract_from_s3()):
        # Conver data weight
        
        return(0)
    
    def clean_products_data(self):
        # import weight converted dataset
        df = self.convert_product_weights()

        # Further clean the data.

        #Return clean dataset.
        return(df)

x = DataCleaning()
print(x.clean_products_data())