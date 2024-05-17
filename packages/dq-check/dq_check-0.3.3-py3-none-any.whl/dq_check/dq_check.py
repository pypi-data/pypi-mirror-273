from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp,current_user,col,lit,cast,collect_list,create_map,row_number
from pyspark.sql.window import Window
from typing import Tuple, Dict, List, Optional
import uuid
import re

class _SparkSQLClient:
    def __init__(self, spark: SparkSession):
        """
        Initialize the SparkSQLClient with a Spark session.

        Args:
            spark (SparkSession): The Spark session to use for SQL execution.
        """
        self.spark = spark
    
    def read_sql(self, sql_query: str):
        """
        Execute the given SQL query using the Spark session.

        Args:
            sql_query (str): The SQL query to execute.

        Returns:
            DataFrame: The result of the SQL query as a PySpark DataFrame.
        """
        try:
            # Execute the SQL query and return the result as a DataFrame
            df = self.spark.sql(sql_query)
            return df
        except Exception as e:
            # Handle any exceptions that occur during SQL execution
            print(f"An error occurred while executing the SQL query: {e}")
            raise e
        

class DQCheck:
    """
    Class for performing data quality checks on a specified table using a given SQL query
    and saving the results into a Delta table for auditing purposes.
    """
    def __init__(self, spark: SparkSession,audit_table_name: str = "audit_log",azure_sql_client = None,run_id:str = '-999'):
        """
        Initialize the DQCheck class.

        Args:
            spark (SparkSession): The Spark session.
            audit_table_name (str): The name of the Delta table to store audit logs.
            azure_sql_client: This is required for asql,create azure_sql_client by providing scope and secret with AzureSQLClient
            run_id:run_id for the ADF pipeline
        """
        self.spark = spark
        self.azure_sql_client = azure_sql_client
        self.audit_table_name = audit_table_name
        self.run_id = run_id

    def parse_sql_query(self,sql_query:str) -> tuple:
        """
        Parse an SQL query and return the list of columns returned and the list of tables involved.

        Args:
            sql_query (str): The SQL query as a string.

        Returns:
            tuple: A tuple containing a list of columns returned in the query and a list of tables involved in the query.
        """
        # Initialize lists for columns and tables
        columns = []
        tables = []

        # Regex pattern to match the SELECT clause
        select_pattern = re.compile(r'SELECT\s+(.*?)\s+FROM', re.IGNORECASE | re.DOTALL)
        # Regex pattern to match the FROM clause
        from_pattern = re.compile(r'FROM\s+(.*?)(?:WHERE|GROUP BY|ORDER BY|$)', re.IGNORECASE | re.DOTALL)
        
        # Extract the SELECT clause
        select_match = select_pattern.search(sql_query)
        if select_match:
            # Extract the columns from the SELECT clause
            select_clause = select_match.group(1)
            # Split the columns by comma and strip whitespace
            columns = [col.strip() for col in select_clause.split(',')]

        # Extract the FROM clause
        from_match = from_pattern.search(sql_query)
        if from_match:
            # Extract the FROM clause
            from_clause = from_match.group(1).strip()

            # Use regex patterns to extract tables
            # This pattern handles table names, aliases, and JOIN clauses
            table_pattern = re.compile(r'((?:\w+\.\w+)?(?:\w+)(?:\s+AS\s+\w+)?(?:\s*JOIN)?(?:\s*\w+\s*)?(?:ON\s)?(?:.*?)(?:=)?)', re.IGNORECASE)
            matches = table_pattern.findall(from_clause)
            # Filter out unnecessary matches
            for match in matches:
                match_split = re.split(r'\s+AS\s+|\s+JOIN\s+|\s+ON\s+', match)
                for part in match_split:
                    # Check for table name and exclude keywords
                    if '.' in part:
                        table_name = part.split('.')[1]
                    else:
                        table_name = part
                    if table_name:
                        # Append table names and exclude empty strings and common keywords
                        if not (table_name in ['', 'AS', 'JOIN', 'ON', '=']):
                            tables.append(table_name)

        # Return the list of columns and tables
        return columns, tables
        
    def perform_dq_check(self,
                         table_type: str,
                         table_name: str,
                         primary_keys: List[str],
                         sql_query: str,
                         where_clause: Optional[str] = None,
                         quality_threshold_percentage: int = 5,
                         chunk_size:int = 200) -> tuple:
        """
        Perform data quality checks on a specified table using a given SQL query and save the results into a Delta table.

        Args:
            table_type (str): The type of the table ('delta' or 'asql').
            table_name (str): The name of the table.
            primary_keys (List[str]): List of primary key columns. 
            sql_query (str): The data quality check query.
            where_clause(str): where clause to get sample data for DQE check
            quality_threshold_percentage (int): Quality threshold percentage (default is 5%).
            chunk_size (int): how many pks per record in audit log table.

        Returns:
        Tuple[str, float]: Tuple containing:
            - Status of the data quality check ('Passed' or 'Failed').
            - Percentage score of failed records.
        
        Appends the resuls of DQ check to Delta table

        """

        # Validate input parameters

        # if not isinstance(self.spark, SparkSession):
        #     raise ValueError("Invalid input: 'spark' must be an instance of SparkSession.")
        
        if table_type not in ['delta', 'asql']:
            raise ValueError("Invalid input: 'table_type' must be 'delta' or 'asql'.")
        
        if not isinstance(table_name, str) or not table_name:
            raise ValueError("Invalid input: 'table_name' must be a non-empty string.")
        
        table_dot_cnt = table_name.count(".")
        if not (table_dot_cnt == 2 or table_dot_cnt == 1):
            raise ValueError("Invalid input: 'table_name' must be a non-empty string and with (catalog and schema name) for delta or with schema name only for asql.")
        
        if not isinstance(primary_keys, list) or not all(isinstance(key, str) for key in primary_keys):
            raise ValueError("Invalid input: 'primary_keys' must be a list of strings.")
        
        if not isinstance(sql_query, str) or not sql_query:
            raise ValueError("Invalid input: 'sql_query' must be a non-empty string.")
        
        if where_clause is not None and not isinstance(where_clause, str):
            raise ValueError("Invalid input: 'where_clause' must be a string if provided.")
        
        if not isinstance(quality_threshold_percentage, int) or quality_threshold_percentage < 0 or quality_threshold_percentage > 100:
            raise ValueError("Invalid input: 'quality_threshold_percentage' must be an integer between 0 and 100.")

        audit_dot_cnt = self.audit_table_name.count(".")
        if not isinstance(self.audit_table_name, str) or not self.audit_table_name or not audit_dot_cnt == 2 :
            raise ValueError("Invalid input: 'audit_table_name' must be a non-empty string and with catalog and schema name.")
        
        #remove colon at end if present
        sql_query = sql_query.replace(';','')
        # Check if the query contains aggregation functions
        aggregates = ['min', 'max', 'avg', 'sum', 'count', 'group by']
        agg_ind = next(('y' for i in aggregates if i in sql_query.lower()), None)
        
        #get catalog,schema,table for DQ table
        table_dtls = table_name.split(".")
        catalog = table_dtls[0] if table_dot_cnt == 2 else None
        schema = table_dtls[-2]
        table_name_only = table_dtls[-1]
        


        #get catalog,schema,table for Audit table table
        audit_table_dtls = self.audit_table_name.split(".")
        audit_catalog = audit_table_dtls[0] if audit_dot_cnt == 2 else None
        audit_schema = audit_table_dtls[-2]
        audit_table_name_only = audit_table_dtls[-1]
        print(F"Audit table catalog,schema,table_name_only: {audit_catalog},{audit_schema},{audit_table_name_only}")

        # Determine the SQL query for data extraction
        if where_clause is None:
                sql_stmt = f"SELECT * FROM {table_name}"
        else:
                sql_stmt = f"SELECT * FROM {table_name} {where_clause}"
                
        print(f"Executing query: {sql_stmt}")

        if (table_type).lower() == 'delta':
            # Create an instance of SparkSQLClient
            client = _SparkSQLClient(self.spark)
        elif (table_type).lower() == 'asql':
            client = self.azure_sql_client
        else:
            print(F"Invalid table type. It should either be delta or asql")

        #create audit schema if not exists
        try:
            if audit_catalog:
                self.spark.sql(F'CREATE SCHEMA IF NOT EXISTS {audit_catalog}.{audit_schema}')
            else:
                self.spark.sql(F'CREATE SCHEMA IF NOT EXISTS {audit_schema}')
        except Exception as e:
            raise Exception(F"User does not have create schema permission for audit table."
                            F"Please make sure audit table schema is available or user has permission to create it."
                            F"Please check error below {e}")

        
        #validate sql

        table_cols,sql_tables = self.parse_sql_query(sql_query)

        # table validation for sample data
        if table_name not in sql_query:
            raise ValueError(f"table {table_name} not in sql from clause {sql_query}")

        
        if '*' not in table_cols:
          #primary key validation
          if set(primary_keys) - set(table_cols):
                  if not agg_ind:
                      agg_without_pk_ind = 'n'
                      raise ValueError(f"primary key {primary_keys} not in sql select clause {table_cols}")
                  else:
                      agg_without_pk_ind = 'y'
          else:
            agg_without_pk_ind = 'n'
        else:
            agg_without_pk_ind = 'n'
        
        print(F"agg_without_pk_ind is {agg_without_pk_ind}")

        #### DQ check logic     

        #get total count from table for batch id
        total_count_sql = f"with sql_sample as ({sql_stmt}) select count(*) as tot_cnt from sql_sample"
        print(F"total count sql:{total_count_sql}")
        #create dq check sql
        #dq_sql = f"with sql_sample as ({sql_stmt}) " + sql_query.replace(table_name,'sql_sample')
        dq_sql_pre = f"with sql_sample as ({sql_stmt}) ," + "dq_check  as " + "(" + sql_query.replace(table_name,'sql_sample') + ")"
        dq_sql = dq_sql_pre + " select * from dq_check"
        print(F"dq_sql:{dq_sql}")
        #get count of records failing dq check
        #dq_count_sql = f"select count(*) as dq_cnt from ({dq_sql})"
        dq_count_sql = dq_sql_pre + " select count(*) as dq_cnt from dq_check"
        print(F"dq_count_sql:{dq_count_sql}")
        #create primary keys for select expression
        primary_keys_str = ','.join(primary_keys)
        #dq_primary_key_sql = F"(select {primary_keys_str} from ({dq_sql}))"
        dq_primary_key_sql = dq_sql_pre + F" select {primary_keys_str} from dq_check"
        print(F"dq_primary_key_sql:{dq_primary_key_sql}")

        df_dq_count = client.read_sql(dq_count_sql)
        df_total_count = client.read_sql(total_count_sql)
        dq_count = list(df_dq_count.first().asDict().values())[0]
        total_count = list(df_total_count.first().asDict().values())[0]

        print(F"dq_cnt and total_cnt are {dq_count} and {total_count}")
        # Calculate percentage score of failed records
        percentage_score = round((dq_count / total_count) * 100,2)
        # Determine the status based on the quality threshold
        if not agg_ind or agg_without_pk_ind == 'n':
            status = "Passed" if percentage_score <= quality_threshold_percentage else "Failed"
        elif dq_count > 0:
            status = "Failed"
        else:
            status = "Passed"
        # Collect primary keys of failed records
        failed_primary_keys = {}
        #failed_primary_keys_sample = {}
        sort_col = primary_keys[0]
        if agg_without_pk_ind == 'n':
            try:
                df_failed_primary_keys = client.read_sql(dq_primary_key_sql)

                #below will be met incase of when there are no failed records.

                if df_failed_primary_keys.count() == 0:
                   df_failed_primary_keys = client.read_sql(F'select "" as {sort_col}') 
                # add all pk cols to df_failed_primary_keys df
                   for pk in primary_keys:
                       if pk != sort_col:
                            df_failed_primary_keys = df_failed_primary_keys.withColumn(pk,lit(''))
            except Exception as e:
                raise KeyError(F"primary keys {primary_keys} are not found in table {table_name}. Please see error below \n {e}")
        else:
            df_failed_primary_keys = client.read_sql(F'select "" as {sort_col}')
                # add all pk cols to df_failed_primary_keys df
            for pk in primary_keys:
                if pk != sort_col:
                    df_failed_primary_keys = df_failed_primary_keys.withColumn(pk,lit(''))

        df_failed_primary_keys = df_failed_primary_keys.withColumn("constant",lit(1))
        window_spec = Window.orderBy("constant")

        df_with_row_number = df_failed_primary_keys.withColumn("Seq",row_number().over(window_spec))
        df_with_chunk = df_with_row_number.withColumn("ChunkNo",((col("Seq")/chunk_size) - 0.05).cast('int') + 1)

        # Apply collect_list dynamically to each column
        agg_exprs = [collect_list(col(column)).alias(column) for column in primary_keys]

        # Group by "ChunkNo" and aggregate using the dynamically created aggregation expressions
        df_aggregated = df_with_chunk.groupBy("ChunkNo").agg(*agg_exprs)

        # Prepare expressions for create_map dynamically
        map_exprs = [(lit(column).alias("Key"), col(column).alias("Value")) for column in primary_keys]

        # Create a single map column for all columns
        map_expr = create_map(*[expr for expr in sum(map_exprs, ())])

        # Add the map column to the DataFrame
        df_mapped_values = df_aggregated.withColumn("FailedRecordsKeys", map_expr)

        audit_log_df = (df_mapped_values.withColumn("UniqueCheckID",lit(str(uuid.uuid4())))
                                .withColumn("RunId",lit(self.run_id))
                                .withColumn("CheckTimestamp",current_timestamp())
                                .withColumn("TableName",lit(table_name))
                                .withColumn("TableType",lit(table_type))
                                .withColumn("QueryUsed",lit(sql_query))
                                .withColumn("Status",lit(status))
                                .withColumn("FailedRecordCount",lit(dq_count))
                                .withColumn("PercentageScore",lit(percentage_score))
                                .withColumn("CurrentUser",current_user())
                                .drop(*primary_keys)
                                .select("UniqueCheckID","RunId","CheckTimestamp","TableName"
                                        ,"TableType","QueryUsed","Status","FailedRecordCount","PercentageScore","FailedRecordsKeys","CurrentUser")
                                )

        print(F"Appending DQE results to table {self.audit_table_name}")    

        # Write the audit log data into the Delta table
        #display(audit_log_df)
        audit_log_df.write.format("delta").option("mergeSchema", "true").mode("append").saveAsTable(self.audit_table_name)


        return(status,percentage_score)