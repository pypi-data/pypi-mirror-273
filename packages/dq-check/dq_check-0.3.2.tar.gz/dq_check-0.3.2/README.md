## dq_check


## Overview

`dq_check` is a Python package that provides a data quality check function encapsulated in the `DQCheck` class. It allows you to perform data quality checks on tables using SQL queries and save the results into a Delta table for auditing purposes.

## Features

- Perform data quality checks on specified tables using SQL queries.
- Save audit logs of data quality checks into a Delta table.
- Handle aggregation checks and basic data quality metrics.
- Supports PySpark and Pandas integration.

## Installation

You can install `dq_check` from PyPI using pip:

## bash

pip install dq_check


## Usage

Here's an example of how to use the DQCheck class from the dq_check package:

from pyspark.sql import SparkSession

from dq_check import DQCheck

## Initialize Spark session
spark = SparkSession.builder.appName("DQCheckExample").getOrCreate()

## Create an instance of DQCheck

dq_checker = DQCheck(spark,audit_table_name) #audit table name should have catalog and schema.

spark (SparkSession): The Spark session.

audit_table_name (str):Default is audit_log. The name of the Delta table to store audit logs.

azure_sql_client:Default is None. This is required for asql,create azure_sql_client by providing scope and secret with AzureSQLClient
            
run_id:Default is -999 , run_id for the ADF pipeline

## Define the data quality check parameters

table_type = "delta"  # Type of the table ('delta' or 'asql')

table_name = "your_table_name"  # Name of the table, should have catalog/schema for delta and schema for asql.

primary_keys = ["your_primary_key"]  # List of primary key columns

sql_query = "SELECT * FROM your_table WHERE condition"  # Data quality check query # should have table name with catalog and schema.

## Perform the data quality check
dq_checker.perform_dq_check(

    table_type,

    table_name,

    primary_keys,

    sql_query,

    where_clause=None, # Optional where clause for sample data

    quality_threshold_percentage=5,  # Optional Quality threshold percentage

    chunk_size=200, #Optional chunk size for pks list
)


## Configuration

Adjust the parameters passed to the perform_dq_check method based on your requirements.

## Dependencies

PySpark
Pandas

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests on the GitHub repository.

## License
None.

## Contact
For any questions or feedback, open a github issue