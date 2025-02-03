from pyspark.sql.catalog import Catalog
from pyspark.sql import SparkSession
import requests

'''
PolarisXCatalog: A Custom PySpark Catalog

By default, `spark.catalog` allows users to:
- List databases, tables, and functions.
- Run `SHOW FUNCTIONS;` to get built-in Spark functions.
- Execute queries using `spark.sql(...)`.

Normally, Spark processes SQL queries using its built-in parser.  
However, `PolarisXCatalog` intercepts queries before Spark runs them:
1. If the query includes `USING PolarisX`, it is sent to the PolarisX API.
2. Otherwise, Spark processes the query as usual.

Example:
```python
spark.catalog.sql("CREATE FUNCTION my_func AS 'return x + 1' USING PolarisX;")

obs. and atm we assume that the Polaris instance contains the object and not just the metadata,
such that we dont have to reconstruct anything.
'''

class PolarisXCatalog(Catalog):
    def __init__(self, spark: SparkSession, api_endpoint: str):
        """
        Custom Catalog for PolarisX that manages functions.
        """
        self.spark = spark
        self.api_endpoint = api_endpoint

    def create_function(self, function_name: str, function_body: str):
        """
        Sends a CREATE FUNCTION request to PolarisX API.
        """
        url = f"{self.api_endpoint}/functions"
        payload = {"name": function_name, "body": function_body}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print(f"Created FUNCTION: {function_name}")
        else:
            print(f"Error creating FUNCTION: {response.text}")

    def show_functions(self):
        """
        Fetches all functions stored in PolarisX.
        """
        url = f"{self.api_endpoint}/functions"
        response = requests.get(url)

        if response.status_code == 200:
            functions = response.json()
            for func in functions:
                print(f"- {func['name']}")
        else:
            print(f"Error fetching FUNCTIONS: {response.text}")
        
    def sql(self, query: str):
        """
        Intercepts SQL queries related to FUNCTIONS and calls the API.
        """
        query_upper = query.strip().upper()

        if query_upper.startswith("CREATE FUNCTION") and "USING POLARISX" in query_upper:
            _, _, function_name, _, function_body, _, _ = query_upper.split(" ", 6)
            self.create_function(function_name, function_body)

        elif query_upper.startswith("SHOW FUNCTIONS") and "USING POLARISX" in query_upper:
            self.show_functions()

        else:
            return self.spark.sql(query)  # Let PySpark handle everything else

