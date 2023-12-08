#!/bin/bash

from database_utils import DatabaseConnector
from data_extraction import DataExtractor


class DataCleaning:

    def clean_user_data(self):
        
        # method to take user data and clean and
        #return the cleaned data for uploading to database.

        # Get data using other methods
        de = DataExtractor()
        table_names = DatabaseConnector().list_db_tables()
        user_table = table_names.index('legacy_users')
        df = de.read_rds_table(table_names[user_table])
        return(df)
    
    
        # Clean user data



    def clean_card_data(self):

        # TO DO creat method too  clean the data to remove any erroneous values, NULL values or errors with formatting.
        # Once cleaned, upload the table with your upload_to_db method to the database in a table called dim_card_details. 
        return(0)
    
    def clean_store_data(self):
        #TO DO.
        return(0)

x =DataCleaning()
print(x.clean_user_data())