# #!/usr/bin/python3
import yaml
from sqlalchemy import create_engine, inspect
from numpy import nan




# Uitlitty classe -------
class DatabaseConnector:

	def read_db_creds(self):
		 # Method to read yaml file with database credential stored.

		 with open('db_creds.yaml', 'r') as file:
			 aws_yaml = yaml.safe_load(file)
		 return(aws_yaml)


	def init_db_engine(self):

		# Method to iniate sqlalcheny databse engine.
		aws_yaml_dict = self.read_db_creds()

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

		# Method to return lsit of all the database tables.

		engine = self.init_db_engine()

		# Context Mananger to automatically disconnect and release resouces
		with engine.execution_options(isolation_level='AUTOCOMMIT').connect() as conn:
			inspector = inspect(engine)

		return(inspector.get_table_names())
	
	def upload_to_db(self, df, table_name, password):
		DATABASE_TYPE = 'postgresql'
		DBAPI = 'psycopg2'
		HOST = 'localhost'
		USER = 'postgres'
		PASSWORD = password
		DATABASE = 'sales_data'
		PORT = 5432

		engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
		engine.connect()
		# Upload pandas dataframe to sql
		df.to_sql(table_name, engine, if_exists='replace')
		
# Utility functions ------
def edit_missing(df):
	# Replcace any Null values with nan in the dataset
	# then check with .info method for any missing vaaues
	df.replace('NULL', nan, inplace = True)
	df.replace(' ', nan, inplace = True)
	df.replace('N/A', nan, inplace = True)
	df.replace('None', nan, inplace = True)
	df.info()	



	


		
