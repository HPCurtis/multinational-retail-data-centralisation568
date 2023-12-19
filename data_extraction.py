#!/usr/bin/python3
from database_utils import DatabaseConnector
import pandas as pd 
from tabula import read_pdf
from  requests import get
from boto3 import client
from os import path

class DataExtractor:
	'''This class extracts sales and accompanying company.business data from various sources.
	'''

	def read_rds_table(self, table_name, dbc = DatabaseConnector()):
		'''Reads table data for give table_name from sql
	 
		Args: 
			table_name(str): Name of table in rds database to read
			dbc(class): Instance of the DatabaseConnector class
		
		Returns:
				DataFrame: rds table as pandas dataframe. 
		'''

		# Generate sqlalechemy engine.
		engine = dbc.init_db_engine()

		table = pd.read_sql_table(table_name, engine)

		# Return pandas dataframe
		return(table)
	
	def retrieve_pdf_data(self, link):
		'''Takes in URL link for pdf file and returns as pandas data frame.

		Args: 
			link(str): url link to where the pdf is stored,
		
		Returns:
				DataFrame: pdf data as pandas dataframe.
		'''
		
		table = pd.concat(read_pdf(link, pages='all'))
		return(table)
	
	def list_number_of_stores(self, ns_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores',
						    api_key = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}):
		'''Requests the number of stores to extract from the associated API

		Args:
			ns_url(str): URL where the number of stores is stored
			api_key(dict): Associated api key with url so the number stores can be retrieved.
		
		Returns:
				int: THe number of stores.
		'''
		# Request number of stores and return response as json.
		response = get(ns_url, headers = api_key).json()
		
		# Returns the number 
		return(response['number_stores'])

	
	def retrieve_stores_data(self, n_stores, store_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/',
						   api_key = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}):
		'''Retreives the store data from associated API provided,

		Args:
			n_store(int): The number of stores.
			store_url(str): URL associated with API that you extract the stores data.
			api_key(dict): Associated api key tobthe url so the number stores can be retrieved.

		Returns:
				DataFrame: Pandas data of stores data.
		'''

		df_list = []
		n_store_list = list(map(str,range(0, n_stores)))
 
		# Loop call the API to get and store all results in a list
		for i in n_store_list:
			response = get(store_url+i, headers = api_key)
			repos_json = pd.json_normalize(response.json())
			df_list.append(repos_json)
		
		'''
		 Concatenate the resulting list into a single pandas dataframe.
		 and return it.
		'''
		df = pd.concat(df_list)
		return(df)
	
	def extract_from_s3(self, address = 's3://data-handling-public/products.csv'):
		'''Extract data from aws s3 bucket address.

		Args:
			address(str): Associated S3 bucket where products data is stored.

		Returns:
				DataFrame: Pandas dataframe of products data
		'''

		# Index the address
		bucket_index_start = address.index('data-handling-public')
		bucket_index_finish = address.index('/p')
		file_name_index_start = bucket_index_finish + 1

		# Extract bucket and file name from address
		bucket_name = address[bucket_index_start:bucket_index_finish]
		file_name = address[file_name_index_start:]
		file_path ='/home/harrison/Desktop/AiCore/multinational-retail-data-centralisation568/'+file_name

		# Check if file exist so call of method does not needlessly dowload the file
		if not path.exists(file_path):
			s3 = client('s3')
			s3.download_file(bucket_name, 
							file_name,
							file_path)
		
		# Get csv into pandas dataframe to be returned below.	
		df = pd.read_csv(file_path)
		return(df)

	def retrieve_events_data(self):
		'''Extract business events data.
		
		Returns:
				DataFrame: Pandas dataframe of events data.
		'''
		df = pd.read_json('https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json')
		
		return(df)
	
