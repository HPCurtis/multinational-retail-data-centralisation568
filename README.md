# Multinational-retail-data-centralisation568


## Project description
This repository contains an illustrative example of SQL database creation and querying tailored for business purposes. The dataset used here simulates sales data from a fictional multinational corporation. The overarching objective is to guide the fictional company in becoming more informed and data-driven in its sales endeavors.

The provided code revolves around the process of gathering sales data from diverse sources, organizing this data into a SQL database (specifically using PostgreSQL), and subsequently executing queries to address a series of business questions related to the sales data.

## Usage instructions

## File structure
The repository contains a series of separate python and sql scripts. The python scripts are broken down into their respective functions.

- database_utils.py contains a series of utility functions that are imported and used through outt the other python scripts.
- data_extraction.py
- data_cleaning.py
- data_upload.py
- scheme_setting.sql contains the sql script to set up the shema for the data base users need only run this once per data upload and then they can then use the business_queries.sql script as they please. 
- business_queries.sql this sql script contains all the sql queries that user can use investigate and answer a series of business questions.

### License 
Copyright [2023] [Harrison Curtis]

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.