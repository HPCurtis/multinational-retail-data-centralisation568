#!/usr/bin/python3

from database_utils import DatabaseConnector, edit_missing
from data_extraction import DataExtractor
from numpy import nan, unique
import pandas as pd


class DataCleaning:

    '''This class cleans extracted sales and accompanying company/business data from various sources.
	'''

    def clean_user_data(self):
       '''Cleans the businesses user data.

       Returns: 
              DataFrame: Cleaned pandas dataframe of users data.  
       '''

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
        '''Cleans the businesses card data.

       Returns: 
              DataFrame: Cleaned pandas dataframe of card data.  
       '''

        # Read in card data for cleaning.
        df = DataExtractor().retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf')

        # Deal with any missing data examples
        edit_missing(df = df)
        df.dropna(inplace = True)

        # Drop nonsense keywords from dataset found in card_provider column.
        keywords = ['NB71VBAHJE', 'WJVMUO4QX6', 'JRPRLPIBZ2',
            'TS8A81WFXV', 'JCQMU8FN85', '5CJH7ABGDR', 'DE488ORDXY', 'OGJTXI6X1H',
            '1M38DYQTZV', 'DLWF2HANZF', 'XGZBYBYGUW', 'UA07L7EILH', 'BU9U947ZGV',
            '5MFWFBZRM9']
        df = df[df.card_provider.isin(keywords) == False]
        
        # Clean up card provider strings.
        df['card_number'] = df['card_number'].astype('string').str.replace('?', '', regex = True)
        # Return the cleaned pandas dataframe.
        return(df)
    
    
    def clean_store_data(self):
        
        '''Cleans the businesses store data.

       Returns: 
              DataFrame: Cleaned pandas dataframe of store data.  
       '''

        
        #Import the store data and reset the index
        df = DataExtractor().retrieve_stores_data(n_stores = DataExtractor().list_number_of_stores())
        df.set_index('index', inplace = True)
        
        # Remove rows based on nonsense words 
        Keywords =  ['ZCXWWKF45G','0OLAK2I6NS', 'A3PMVM800J', 'GMMB02LA9V', '13PIY8GD1H', '36IIMAQD58', '7AHXLXIUEF']
        df = df[df.opening_date.isin(Keywords) == False]
        
        # Strip all non numric value from staff_members.
        df['staff_numbers'] = df['staff_numbers'].str.extract(pat='(\d+)', expand=False)
    
        return(df)
    
    def clean_orders_data(self):
       '''Cleans the businesses order data.

       Returns: 
              DataFrame: Cleaned pandas dataframe of order data.  
       '''

        # Import data frame for cleaning.
       df = DataExtractor().read_rds_table('orders_table')
       df.set_index('index', inplace = True)
       print(df.iloc[0])

        # Clean data
        # Drop the first name, last name and 1 columns from dataframe
       df.drop(['first_name', 'last_name', '1'],  inplace =True , axis=1)
        
        # Check show missing values in the dataset
        # There is non.
       edit_missing(df)

       return(df)

    
    def convert_product_weights(self, df = DataExtractor().extract_from_s3()):
        '''
        import data from aws s3 bucket and then converts
        the weight column so all values are on the kg scale,

       Returns: 
              DataFrame: pandas dataframe with weight column set to kg.  
       
        '''
        
        df.info()
        # Get weight into pandas series without na values
        #df['weight'] = df['weight'].str.rstrip('kg')
        weights = df.weight 

        # Switch all ml to grams as one to one ratio.
        weights = weights.str.replace('ml', 'g')

        #Convert the unique ounc score to kg 
        weights = weights.str.replace('16oz', '0.45kg')
        
        #Gnerate dataset witnout na values for use below.
        weights_na = weights.dropna()

        # Weight conversion.
        # Convert the srting with multplcation insidede
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
        
        df.loc[weights.index, 'weight'] = weights 
        
        df.loc[weight_x_string_split_df['weight_kg'].index, 'weight'] = weight_x_string_split_df['weight_kg']
        
        df.loc[weight_g_string.index, 'weight'] = weight_g_string

        # Convert to sting and remove any with kg suffixes.
        df['weight'] = df.weight.astype('string')
        df['weight'] = df.weight.str.replace('kg', '')

        return(df)
    

    def clean_products_data(self):
       '''Cleans the businesses prodcuts data.

       Returns: 
              DataFrame: Cleaned pandas dataframe of products data.  
       '''

        # import weight converted dataset
       df = self.convert_product_weights()
       df.rename(columns = {'EAN': 'ean'}, inplace = True)
       edit_missing(df = df)
        
        # Remove missing values
       df.dropna(inplace = True) 
       df.info()
        
       df = df[ df.uuid.str.contains(pat = '-')]

        #Return clean dataset.
       return(df)
    
    def clean_events_data(self):
       '''Cleans the events data.

       Returns: 
              DataFrame: Cleaned pandas dataframe of events data.  
       '''
        # retrieve events data using DataExtractor class
       df = DataExtractor().retrieve_events_data()
        # Cnvert to string.
       df['date_uuid'] = df['date_uuid'].astype('string')
       df['date_uuid'] = df['date_uuid'].str.strip()
        
        #Deal with missing values
        # Timestamp regex
       regex_expression =  r'\d\d:\d\d:\d\d'

        # Values that dont follow timestamp convert to numpy nan.
       df.loc[~df['timestamp'].str.match(regex_expression), 'timestamp'] = nan
        # DRop null vales
       edit_missing(df)
       df.dropna(inplace = True)

        # Remove rows with unidentifiable key words from dataframe.
       includeKeywords = ['DXBU6GX1VC', 'OEOXBP8X6D',
                            '1Z18F4RM05', 'GT3JKF575H', 'CM5MTJKXMH', '5OQGE7K2AV', '1JCRGU3GIE',
                            'SQX52VSNMM', 'ALOGCWS9Y3', '7DNU2UWFP7', 'EOHYT5T70F', '5MUU1NKRED',
                            '7RR8SRXQAW', 'SSF9ANE440', '1PZDMCME1C', 'KQVJ34AINL', 'QA65EOIBX4',
                            'YRYN6Y8SPJ', 'JMW951JPZC', 'DZC37NLW4F', 'SYID3PBQLP', 'IXNB2XXEKB',
                            'MZIS9E7IXD']

       df = df[df.time_period.isin(includeKeywords) == False]

        # Clean data
       return(df)




