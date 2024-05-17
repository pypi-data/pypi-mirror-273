# PyHasura

A library for conveniently working with Hasura, GraphQL, File Formats, and some basic Machine Learning.

## Getting Started

### HasuraClient

```python

# Create Hasura Client
import os
from dotenv import load_dotenv
from pyhasura import gql_client, HasuraClient, ExportFormat
from pprint import pprint

load_dotenv()  # Load environment variables from .env

hasura_client = HasuraClient(uri=os.environ.get("HASURA_URI"), admin_secret=os.environ.get("HASURA_ADMIN_SECRET"))
```

### Query for a Result

```python
result = hasura_client.execute("""
        query findCarts {
            carts {
                is_complete
                cart_items {
                    quantity
                    product {
                        price
                    }
                }
            }
            cart_items {
                id
            }
        }
    """)

pprint(result)
```

### Convert Results to a Dictionary of Alternate Formats

```python
result = hasura_client.convert_output_format(ExportFormat.ARROW)
pprint(result)
result = hasura_client.convert_output_format(ExportFormat.CSV)
pprint(result)
result = hasura_client.convert_output_format(ExportFormat.PARQUET)
pprint(result)
result = hasura_client.convert_output_format(ExportFormat.DATAFRAME)
pprint(result)
result = hasura_client.convert_output_format(ExportFormat.FLAT)
pprint(result)
```

### Write Results, one file for each root entry in the query
```python
result = hasura_client.write_to_file(output_format=ExportFormat.ARROW)
pprint(result)
result = hasura_client.write_to_file(output_format=ExportFormat.CSV)
pprint(result)
result = hasura_client.write_to_file(output_format=ExportFormat.PARQUET)
pprint(result)
result = hasura_client.write_to_file(output_format=ExportFormat.FLAT)
pprint(result)
result = hasura_client.write_to_file(output_format=ExportFormat.NATURAL)
pprint(result)
```

### Detect Anomalies

Uses Doc2Vec to facilitate deeper semantic analysis, but also works fine with categorical string fields.

```python
result = hasura_client.anomalies()
pprint(result)
result = hasura_client.anomalies(threshold=.03)
pprint(result)
```

### Train and Serialize then Re-Use for Anomaly Detection

Typically, do this to train on some historical dataset and then
search for anomalies in an alternate (maybe current) dataset.
```python
result = hasura_client.anomalies_training()
pprint(result)
result = hasura_client.anomalies(training_files=result, threshold=0)
pprint(result)
```

### Clustering

Uses KMedoids clustering. You are always working on a dictionary of datasets.
You need to define the number of clusters for each dataset in a corresponding input dictionary.
You can auto-generate the optimal number of clusters and use that as the input.
```python
result = hasura_client.optimal_number_of_clusters(1,8)
pprint(result)
result = hasura_client.clusters(result)
pprint(result)
```

### Model First Design using DBML

Build models using [DB Diagram](https://dbdiagram.io/) then generate Hasura metadata.
```python
metadata = hasura_client.add_dbml_model_as_source(
    'global-retail-sales.dbml',
    kind='postgres',
    configuration=configuration,
    output_file='new-metadata.json'
)
```

### Auto-Generated/Discovery of Relationships

Wire up as many data sources as you want to analyze to a Hasura instance
and automatically generate relationships (across data sources).
```python
old_metadata = hasura_client.get_metadata()

# generate relationships
new_metadata = hasura_client.relationship_analysis('new-metadata.json', entity_synonyms={"Stores": ["warehouse"]})

# update hasura with new relationships
hasura_client.replace_metadata(metadata=new_metadata)

```

### Upload a folder of CSVs to PostgreSQL

Create a datasource from a schema from PostgreSQL.
Point a folder of CSVs to same PostgreSQL instance and schema.
Then automatically track them in Hasura.

```python
# upload data to database
tables = hasura_client.upload_csv_folder('retailer', uri=_uri, casing=Casing.camel)

# track all the tables we uploaded
result = hasura_client.track_pg_tables(tables, schema="public")
```
