#!/bin/python3
from database_utils import DatabaseConnector
import pandas as pd 
import tabula
import requests
import boto3

class DataExtractor:
	

	def read_rds_table(self, table_name, dbc = DatabaseConnector()):

		# generate sqlalechemy engine.
		engine = dbc.init_db_engine()

		#with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
		table = pd.read_sql_table(table_name, engine)

		# return pandas dataframe
		return(table)
	
	def retrieve_pdf_data(self, link):
		#Mehtod to return pdf data as pandas dataframe. 
		table = pd.concat(tabula.read_pdf(link, pages='all'))
		return(table)
	
	def list_number_of_stores(self, ns_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores',
						    api_key = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}):
		response = requests.get(ns_url, headers = api_key).json()
		#Inmdecxing ight not be neccesary
		return(response['number_stores'])

		# This will show the number of stores.
		return(response.text)
	
	def retrieve_stores_data(self, n_stores, store_url = 'https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/',
						   api_key = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}):
	
		df_list = []
		n_store_list = list(map(str,range(0, n_stores)))

		for i in n_store_list:
			response = requests.get(store_url+i, headers = api_key)
			repos_json = pd.json_normalize(response.json())
			df_list.append(repos_json)
		
		df = pd.concat(df_list)
		return(df)
	
	def extract_from_s3(self):
		return(0)

#x = DataExtractor()
#table_name = DatabaseConnector().list_db_tables()[1]
#print(x.read_rds_table(table_name=table_name))
