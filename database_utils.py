#!/usr/bin/python3

# Import required packages.
import yaml
from sqlalchemy import create_engine, inspect
from numpy import nan
import pandas as pd

class DatabaseConnector:
	'''This class reads various yaml files in order to generate sqlalchemy engines 
	for the use in extraction, cleaning and uploading of that data to a PostgresSQL
	database.
	'''

	def read_db_creds(self, filename):
		''' Reads db_cred.yaml file.

		Args:
			filename (str): Name of yaml file you wish to read. 
		
		Returns: 
				dict: of database credentials
		'''

		with open(filename, 'r') as file:
			 yaml_file = yaml.safe_load(file)
		return(yaml_file)


	def init_db_engine(self):
		'''Takes dictionary returned from read_db_creds method and initialises and sqlaclemy engine.
		
		Returns:
				class: instance of sqlalchemy database engine class.
		'''
		aws_yaml_dict = self.read_db_creds('db_creds.yaml')

		DATABASE_TYPE = 'postgresql'
		DBAPI = 'psycopg2'
		HOST = aws_yaml_dict['RDS_HOST']
		USER = aws_yaml_dict['RDS_USER']
		PASSWORD = aws_yaml_dict['RDS_PASSWORD']
		DATABASE = aws_yaml_dict['RDS_DATABASE']
		PORT = aws_yaml_dict['RDS_PORT']

		# Create sqlalchemy engine.
		db_engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
		return(db_engine)
	
	def list_db_tables(self):

		'''Uses sqlaclhemy to get list database tables.

		Returns: 
				list: list of table names of the database.
		'''

		# Initialise sqlalchemy engine.
		engine = self.init_db_engine()

		# Context Manager to automatically disconnect and release resources
		with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
			inspector = inspect(engine)

		return(inspector.get_table_names())
	
	def upload_to_db(self, df, table_name, password):
		'''Uploads pandas dataframe to postgres database.

		Args:
			df: pandas dataframe.
			table_name: Name of table to be set in the postgres database
			password: password to connect to postgres database.

		Returns:
				None
		'''

		# Specification of Database intitised seperately in pgAdmisions.
		DATABASE_TYPE = 'postgresql'
		DBAPI = 'psycopg2'
		HOST = 'localhost'
		USER = 'postgres'
		PASSWORD = password
		DATABASE = 'sales_data'
		PORT = 5432

		# Generate sql engine.
		engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
		engine.connect()

		''' 
		Upload pandas dataframe to sql. 
		if_exists set to 'replace' overwrite data tables 
		that names already exist with data from source.
		'''
		df.to_sql(table_name, engine, if_exists='replace')
		
# Utility functions ------
def edit_missing(df):
	'''Takes pandas dataframe and replaces all standard non-identifable 
	null values to pandas and converts them numpy nan inplace so they can be recognised by 
	pd.dropna(). 

	Args: 
		df: Pandas dataframe 

	Returns:
			None
	'''

	# Replace any Null values with nan in the dataset
	# then check with .info method for any missing vaaues
	df.replace('NULL', nan, inplace = True)
	df.replace(' ', nan, inplace = True)
	df.replace('N/A', nan, inplace = True)
	df.replace('None', nan, inplace = True)
	df.info()	

