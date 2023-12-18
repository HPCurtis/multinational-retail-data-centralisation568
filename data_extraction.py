#!/bin/python3
from database_utils import DatabaseConnector
import pandas as pd 
import tabula
import requests
import boto3
import os

filename = 'db_creds.yaml'

class DataExtractor:
	

	def read_rds_table(self, table_name, dbc = DatabaseConnector()):
		''' '''

		# generate sqlalechemy engine.
		engine = dbc.init_db_engine()

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
	
	def extract_from_s3(self, address = 's3://data-handling-public/products.csv'):
		# Index the address
		bucket_index_start = address.index('data-handling-public')
		bucket_index_finish = address.index('/p')
		file_name_index_start = bucket_index_finish + 1

		# Extract bucket and file name from address
		bucket_name = address[bucket_index_start:bucket_index_finish]
		file_name = address[file_name_index_start:]
		file_path ='/home/harrison/Desktop/AiCore/multinational-retail-data-centralisation568/'+file_name

		# Check if file exist so call of method does not needlessly dowload the file
		if not os.path.exists(file_path):
			s3 = boto3.client('s3')
			s3.download_file(bucket_name, 
							file_name,
							file_path)
		
		# Get csv into pandas dataframe to be returned below.	
		df = pd.read_csv(file_path)
		return(df)

	def retrieve_events_data(self):
		df = pd.read_json('https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json')
		
		return(df)
	

