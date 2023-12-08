# #!/usr/bin/python3
import yaml
from sqlalchemy import create_engine, inspect
import psycopg2



class DatabaseConnector:


	def read_db_creds(self, filename):
		 # Method to read yaml file with database credential stored.

		 with open(filename, 'r') as file:
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
	
	def upload_to_db(self, pd_df, table_name):

		#Method to upload cleaned data to sql database
		return 0
	
#x = DatabaseConnector().list_db_tables()


		
