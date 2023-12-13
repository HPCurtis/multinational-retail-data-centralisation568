#!/bin/bash

from database_utils import DatabaseConnector, edit_missing
from data_extraction import DataExtractor
from numpy import nan
import pandas as pd

filename = 'db_creds.yaml'

class DataCleaning:

    def clean_user_data(self):
       # Import data 
       df = DataExtractor().read_rds_table('legacy_users')
       #df.drop(columns= 'index', inplace = True)
       df.reset_index(drop=True)
       # Clean the data

       # Get rid of redundant rows that do not contain UUID's formated values without '-' 
       df = df[ df.user_uuid.str.contains(pat = '-')]
       

       # Replcace any NUll values with nan in the dataset
       # then check with .info method for any missing vaaues
       edit_missing(df = df)

       #Remove missing values
       df.dropna(inplace = True) 

       # Fix address'
       # Note the issue with comma on final part are untouched as no way to know 
       # what they are and maybe attempt at privacy at input
       # Fix layout with the replacment of comma
       df.address = df.address.str.replace(',', '\\') 
      
      
       # To DO find a solution to phone number issue using pandas.    
       return(df)


    def clean_card_data(self):
        
        #Import card data for cleaning.

        # Deal with any missing data examples
        df = DataExtractor().retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')
        edit_missing(df = df)
        df.dropna(inplace = True)

        df = df[ df.date_payment_confirmed.str.contains(pat = '-')]
        return(df)
    
    
    def clean_store_data(self):
        #Import store data
        df = DataExtractor().retrieve_stores_data(n_stores = DataExtractor().list_number_of_stores())
        df.set_index('index', inplace = True)

        # Get rid of non-numeric latitude values specify as null to be dealt wtih in sql 
        # as specified by task.
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        # Store lat values to be reinserted
        lat_na = df['lat']
        df.drop(columns= 'lat', inplace = True)

        # Strip no numric value from staff_members.
        df['staff_numbers'] = df['staff_numbers'].str.extract(pat='(\d+)', expand=False)
        

        # Remove missing values 
        edit_missing(df = df)
        df.dropna(inplace = True)

        # Reinsert lat column sql task
        df['lat'] = lat_na
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
    
    # TO DO finish this task.
    def convert_product_weights(self, df = DataExtractor().extract_from_s3()):
        df.info()
        # Get weight into pandas series without na values
        #df['weight'] = df['weight'].str.rstrip('kg')
        weights = df.weight 

        # Switch all ml to grams as one to one ratio.
        weights = weights.str.replace('ml', 'g')

        #Convert the unique ounc score to kg 
        weights = weights.str.replace('16oz', '0.45kg')

        weights_na = weights.dropna()

        # Weight conversion.
        #Conver the srting with multplcation insidede
        x_str_mask = weights_na.str.contains('x')
        weight_x_string = weights_na[x_str_mask].str.replace('g', '')
        weight_x_string_split = weight_x_string.str.split(expand= True)
        weight_x_string_split_df = pd.DataFrame(weight_x_string_split)
        weight_x_string_split_df[0],  weight_x_string_split_df[2] = weight_x_string_split_df[0].astype('int'), weight_x_string_split_df[2].astype('int')
        weight_x_string_split_df['weight_kg'] = (weight_x_string_split_df[0] * weight_x_string_split_df[2]) /1000

        # Extract gram values
        g_str_mask = weights_na.str.contains('kg')
        weight_g_string = weights_na[~g_str_mask]
        weight_g_string = weight_g_string[~x_str_mask]
        weight_g_string = weight_g_string.str.replace('g', '')
        weight_g_string = weight_g_string.str.replace(' .', '')

        # Get rid word of nosnes values
        # Note still need to be cleaned later  
        weight_g_string = weight_g_string.drop(weight_g_string[weight_g_string.str.len() >= 8].index )
        
        # Convert grams to KG 
        weight_g_string = weight_g_string.astype('float') / 1000
        # #Convert back to string for replacment below
        weight_g_string = weight_g_string.astype('string')
        
        
        # #This works
        df.loc[weights.index, 'weight'] = weights 
        
        df.loc[weight_x_string_split_df['weight_kg'].index, 'weight'] = weight_x_string_split_df['weight_kg']
        
        df.loc[weight_g_string.index, 'weight'] = weight_g_string

        df['weight'] = df.weight.astype('string')
        df['weight'] = df.weight.str.replace('kg', '')

        return(df)
    

    def clean_products_data(self):
        # import weight converted dataset
        df = self.convert_product_weights()
        edit_missing(df = df)
        
        #Remove missing values
        df.dropna(inplace = True) 
        df.info()
        

        df = df[ df.uuid.str.contains(pat = '-')]
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
        # cols=["year","month","day"]
        # df['date'] = df[cols].apply(lambda x: '-'.join(x.values.astype(str)), axis="columns")

        df = df[ df.date_uuid.str.contains(pat = '-')]

        # Drop useless columsn now datetime is set.
        # df.drop(columns = cols, inplace = True)


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
        
#x = DataCleaning().clean_products_data()
#print(x)
