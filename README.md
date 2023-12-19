<h1> Multinational-retail-data-centralisation568</h1>

<h1> Table of Contents</h1>

- [Project description](#project-description)
- [File structure](#file-structure)
- [Installation instructions](#installation-instructions)
- [Usage instructions](#usage-instructions)
- [License](#license)


## Project description
This repository contains an illustrative example of SQL database creation and querying tailored for business purposes. The data here is hypothetical sales data from a fictional multinational corporation. The overarching objective is to guide the fictional company in becoming more informed and data-driven in its sales endeavors.

The provided code revolves around the process of gathering the said sales data from the companies diverse sources (primairliy AWS sources), organizing this data into a SQL database (specifically using PostgreSQL), and subsequently executing a set of queries to address a series of business questions related to the sales data.

## File structure
This repository contains a series of separate python and sql scripts. The python scripts are broken down into their respective general functionality of extracting, cleaning and uploading the data. In addition to utility functions. The sql scripts function to set the database schema and answer a set of busniess queries.

*Python*
- database_utils.py contains a series of utility Classes/functions that are imported and used through out the other python scripts.
- data_extraction.py contains the DataExtractor class whci hcontains a series of methods to extarct the companies data from the various sources required.
- data_cleaning.py contains the DataCleaning class which cleans all data extracted from the various sources.
- data_upload.py this script seperately calls the upload_db method from database_utils class of DatabaseConnector to upload each cleaned dataframe to the designated Postgres database dsicsused in usage instructions [here](#usage-instructions).

*SQL*
- schema_setting.sql is the sql script to set up the shema for the data base users need only run this once per data upload and then they can then use the business_queries.sql script as they please. 
- business_queries.sql this sql script contains all the sql queries that user can use to investigate and answer a series of business questions asked of the company.

*Addtional*
To make the scripts run you need two additonal yaml files. The first is databse credentials for an AWS RDS SQL database that is contained in yaml file called db_creds.yaml that  only availibbe to people with permission to have the file from AiCore company [here](https://www.theaicore.com/). The second is a user generated file called upload_db_creds.yaml that must contain password of users choosing when creating the sales_data database.

The pload_db_creds.yaml file only needs it to say - PASSWORD: insert password of users choosing

## Installation instructions 
*Python* 

To utilize the provided scripts, users are required to install Python. Instructions for downloading and installing Python can be found at [Python's official website](https://www.python.org/downloads/). Additionally, it is recommended that users also download and install Conda, a package manager and environment management tool. Instructions for Conda installation can be found [here](https://docs.conda.io/projects/conda/en/stable/user-guide/install/download.html).

By installing Conda, users can easily create a dedicated Conda environment that includes all the necessary Python packages required to execute the scripts seamlessly.


*Required python packages*

(Pandas, Numpy, boto3, pyyaml, sqlalchemy, tabula, requests, os)

*SQL*
For running the SQL scripts, users need to download and set up PostgreSQL along with PGAdmin. Follow the links below for downloading:

1. **PostgreSQL:**
   - Download from: [PostgreSQL Official Website](https://www.postgresql.org/download/)

2. **PGAdmin:**
   - Download from: [PGAdmin Official Website](https://www.pgadmin.org/download/)

Ensure to complete the installations for both PostgreSQL and PGAdmin. These tools are essential for managing the SQL database and executing the SQL scripts effectively.

## Usage instructions

To use the code found in the repository users must first set up a Postgres Server and the SQL database called sales_data. This most easily achieved using PGAdmin. This database must be set up so it matches these variable setting required of sqlalchemy engine creation. 

```
  HOST = 'localhost'
  USER = 'postgres'
  PASSWORD = password
  DATABASE = 'sales_data'
  PORT = 5432
```

The two passwords required in the scripts are found in two yaml the first of these files contains databse credentials for an AWS RDS SQL database that is contained in yaml file called db_creds.yaml. This file  only availibbe to people with permission to have the file from AiCore company [here](https://www.theaicore.com/).

The second is a user generated yaml file that must be called upload_db_creds.yaml that must contain the password of users choosing when creating the sales_data database. The upload_db_creds.yaml file only needs it to say.
```
PASSWORD: 'password of users choosing'
```

With that all correct users will only need to run data_upload.py file to upload the data onto their postgres sales_data database. If that runs fine users can simple move on to using the sql scripts. This will require users to once and only once per initialsation of sales_data to run the schema.sql file. This will set the database schema correctly.

From here users can use the business_queries.sql file to run any of database queries in PGadmin to query the data to answer a set of business questions outlined in the script.

## License 
Copyright [2023] [Harrison Curtis]

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.