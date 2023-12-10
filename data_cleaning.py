#!/bin/bash

from database_utils import DatabaseConnector, edit_missing
from data_extraction import DataExtractor
from numpy import nan

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

       # Replcace any NUll values with nan in the dataset
       # then check with .info method for any missing vaaues
       edit_missing(df = df)
       #TO DO add dropna method to get rid of NA's
       df.dropna(inplace = True) 
       
       # Fix address'
       # Note the issue with comma on final part are untouched as no way to know 
       # what they are and maybe attempt at privacy at input
       # Fix layout with the replacment of comma
       df.address = df.address.str.replace(',', "\\") 
      
       # To DO find a solution to phone number issue using pandas.    
       return(df)


    def clean_card_data(self):
        
        #Import card data for cleaning.

        # Deal with any missing data examples
        df = DataExtractor().retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
        edit_missing(df = df)
        return(df)
    
    
    def clean_store_data(self):
        #Import store data
        df = DataExtractor().retrieve_stores_data(n_stores = DataExtractor().list_number_of_stores())
        df.set_index('index', inplace = True)

        # Remove missing values 
        edit_missing(df = df)

        # The lat columns is essential empty so drop from datafraem
        # If that data is required it is avaible at source
        df.drop(columns=['lat'], inplace = True)
        df.dropna(inplace = True)
        
        # Drop nonsense row
        df.drop(447, inplace  = True)

        return(df)
    
    def clean_products_data(self):
        df = convert_product_weights() 
        return(df)
    
    def clean_orders_data(self):
        # Import data fraem for cleaning.
        df = DataExtractor().read_rds_table('orders_table')
        df.set_index('index', inplace = True)

        # Clean data
        # Drop the first name, last name and 1 columns from dataframe
        df.drop(['first_name', 'last_name', '1'],  inplace =True , axis=1)
        
        # Check show missing values in the dataset
        edit_missing(df)

        # return cleaned dataframe.
        return(df)
    
    def convert_product_weights(self, df = DataExtractor().extract_from_s3()):
        # Get weight into pandas series without na values
        weights = df.weight 
        # Cacualte the max string lenght for use below
        max_string_length = weights.str.len().max()

        # Calculate nubmer of Na values.
        number_of_na = weights.isna().sum()

        # Remove na values and non weight values and generate new dataframe.
        weights_na = weights.dropna()
        weights_na.drop(weights[weights.str.len() >= max_string_length].index, inplace = True)

        # Weight conversion.
        
        x_str_mask = weights_na.str.contains('x')

        weight_x_string = weights_na[x_str_mask]
       # weight_kg = weights[~x_str_mask]

        return(weight_x_string)
        

    
    def clean_products_data(self):
        # import weight converted dataset
        df = self.convert_product_weights()
        
        # Further clean the data.

        #Return clean dataset.
        return(df)
    
    def clean_events_data(self):
        # retrieve events data using DataExtractor class
        df = DataExtractor().retrieve_events_data()
        #Deal with missing values
        edit_missing(df)
        df.dropna(inplace = True)

        # Combine the day month year into datetime fore consistency
        cols=["year","month","day"]
        df['date'] = df[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")

        # Drop useless columsn now datetime is set.
        df.drop(columns = cols, inplace = True)


        # Remove rows with unidentifiable key words from dataframe.
        includeKeywords = ['DXBU6GX1VC', 'OEOXBP8X6D',
                            '1Z18F4RM05', 'GT3JKF575H', 'CM5MTJKXMH', '5OQGE7K2AV', '1JCRGU3GIE',
                            'SQX52VSNMM', 'ALOGCWS9Y3', '7DNU2UWFP7', 'EOHYT5T70F', '5MUU1NKRED',
                            '7RR8SRXQAW', 'SSF9ANE440', '1PZDMCME1C', 'KQVJ34AINL', 'QA65EOIBX4',
                            'YRYN6Y8SPJ', 'JMW951JPZC', 'DZC37NLW4F', 'SYID3PBQLP', 'IXNB2XXEKB',
                            'MZIS9E7IXD']

        df_red = df[df.time_period.isin(includeKeywords) == False]
        
        # CLean data
        return(df)
        
        #return(df.time_period.unique(), )

