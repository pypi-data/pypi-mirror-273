import base64
import copy
import json
import os
import pickle
import tempfile
from enum import Enum

import pandas as pd
import pyarrow as pa
import requests
from gql import gql
from graphql import build_client_schema
from pymongo import MongoClient
from sklearn.ensemble import IsolationForest
from sklearn.feature_extraction import DictVectorizer
from sklearn_extra.cluster import KMedoids

from pyhasura import gql_client, flatten_nested_dicts
from pyhasura.helpers import get_ordinal_of_smallest_number, compute_deltas
from pyhasura.relationships import Relationships
from pyhasura.upload_csvs import import_tables, Casing
from pyhasura.vectorize import vectorize_dicts
from pyhasura.dbml_hasura import add_dbml
from gql.transport.requests import log as requests_logger


class ExportFormat(Enum):
    FLAT = 1
    DATAFRAME = 2
    ARROW = 3
    NATURAL = 4
    PARQUET = 5
    CSV = 6


def add_score(item, index, score):
    copy = dict(item)
    copy['__score__'] = score
    copy['__index__'] = index
    return copy


def add_dummy_features(dicts, n, m):
    for d in dicts:
        z = m
        while len(d) < n and z != 0:
            # Add dummy features with default values (e.g., 0)
            dummy_key = f'dummy_feature_{len(d)}'
            d[dummy_key] = 0
            z = z - 1
    return dicts


def create_empty_arrays(n):
    return [[] for _ in range(n)]


class HasuraClient:
    """

    """

    def __init__(self, uri=None, role=None, admin_secret=None, output_dir='.', headers=None, logging_=None):
        """
        Args:
            uri (str): The URI for the GraphQL server.
            role (str, optional): The role to be used for Hasura authorization. Defaults to None.
            admin_secret (str, optional): The Hasura admin secret. Defaults to None.
            output_dir (str, optional): The directory where output files will be saved. Defaults to '.'.
            headers (dict, optional): Additional headers to be included in the GraphQL request. Defaults to None.
            logging_ (bool, optional): Whether to enable logging. Defaults to None.

        """
        if headers is None:
            headers = {}
        if role is not None:
            headers['x-hasura-role'] = role
        if admin_secret is not None:
            headers['x-hasura-admin-secret'] = admin_secret
        self.uri = uri
        self.admin_secret = admin_secret
        if uri is not None:
            self.client = gql_client(self.uri, headers=headers)
        if logging_ is not None:
            self.logging = logging_
        self.result = {}
        self.native_result = {}
        self.vectorized_result = {}
        self.anomalies_result = {}
        self.output_dir = output_dir
        self.result_format = None
        self.operation_name = None
        self.extensions: dict = {}
        self.metadata = {}
        requests_logger.setLevel(self.logging.ERROR)

    def _transform_to_flatten(self):
        flatten_result = {key: flatten_nested_dicts(val) for key, val in self.native_result.items()}
        return flatten_result

    def _transform_to_dataframe(self):
        flatten_result = {key: pd.DataFrame(flatten_nested_dicts(val)) for key, val in self.native_result.items()}
        return flatten_result

    def _transform_to_arrow(self):
        flatten_result = {key: pa.Table.from_pandas(pd.DataFrame(flatten_nested_dicts(val))) for key, val in
                          self.native_result.items()}
        return flatten_result

    def execute(self, query, variables=None, output_format=ExportFormat.NATURAL, operation_name=None):
        op = gql(query)
        operation_name = operation_name if operation_name is not None else op.definitions[0].name.value
        result = self.client.execute(gql(query), variables, operation_name=operation_name, get_execution_result=True)
        self.extensions = result.extensions
        self.native_result = result.data
        self.result = self.native_result
        self.operation_name = operation_name
        return self.convert_output_format(output_format)

    def _get_file_path(self, extension):
        return os.path.join(self.output_dir, extension)

    @staticmethod
    def _write_result_as_file(file_name, result_data):
        with open(file_name, 'w') as file:
            json.dump(result_data, file, indent=4)

    def set_data(self, data, output_format=ExportFormat.NATURAL, operation_name=None):
        """
        Set the data for the current instance.

        Args:
            data: The data to be set for the instance.
            output_format: The output format to be used for the data (default is ExportFormat.NATURAL).
            operation_name: An identifier for the operation that generated the dataset (default is None)

        Returns:
            The converted data based on the specified output format.
        """
        self.native_result = data
        self.result = self.native_result
        self.operation_name = operation_name
        return self.convert_output_format(output_format)

    def get_metadata(self):
        """Gets the metadata for the given object.

        This method makes a request to the specified URI to retrieve the metadata for the object.
        It replaces the 'graphql' path with 'metadata' in the URI and sends a POST request with the
        admin secret header to get the metadata. The metadata is stored in the `metadata` attribute
        of the object and a deep copy of the metadata is returned.

        Returns:
            A deep copy of the metadata for the object.
        """
        self.metadata = json.loads(requests.post(self.uri.replace('graphql', 'metadata'),
                                                 headers={'x-hasura-admin-secret': self.admin_secret}).text)
        return copy.deepcopy(self.metadata)

    def reload_schema(self):
        """
        Reloads the schema by sending a GET request to the hasura proxy server.

        Returns:
            response (requests.Response): The response object containing the server's response.
        """
        return requests.get(self.uri.replace('graphql', 'reload-schema'))

    def relationship_analysis(
            self,
            filename=None,
            entity_synonyms=None,
            alternate_keys=None,
            key_suffixes=None,
            key_uniqueness_test_size=10000,
            key_uniqueness_test_rate=.2,
            key_correlation_test_size=300000,
            key_correlation_test_rate=.05,
    ):
        """
        Args:
            filename: The name of the file to save the metadata analysis results. If not specified, the results will not be saved to a file.
            entity_synonyms: A dictionary containing entity synonyms to be used in the analysis. Each key-value pair represents a synonym mapping, where the key is the original entity name and
        * the value is the synonym.
            alternate_keys: A list of alternate keys to consider in the analysis. Each alternate key is a list of entity attributes that should uniquely identify an entity.
            key_suffixes: A list of suffixes to add to the names of the keys to be tested for uniqueness and correlation. Each suffix should be a string.
            key_uniqueness_test_size: The number of entity records to sample for testing key uniqueness. Default is 10000.
            key_uniqueness_test_rate: The ratio at which to sample entity records for testing key uniqueness. Default is 0.2 (20%).
            key_correlation_test_size: The number of entity records to sample for testing key correlation. Default is 300000.
            key_correlation_test_rate: The ratio at which to sample entity records for testing key correlation. Default is 0.05 (5%).

        Returns:
            metadata: A dictionary containing the relationship analysis results.

        """
        rel = Relationships(
            self.get_metadata(),
            self.get_schema(),
            logging_=self.logging,
            client=self,
            alternate_keys=alternate_keys,
            key_suffixes=key_suffixes,
            entity_synonyms=entity_synonyms,
            key_uniqueness_test_size=key_uniqueness_test_size,
            key_uniqueness_test_rate=key_uniqueness_test_rate,
            key_correlation_test_size=key_correlation_test_size,
            key_correlation_test_rate=key_correlation_test_rate
        )
        metadata = rel.analyze_relationships()
        if filename is not None:
            with open(filename, 'w') as f:
                json.dump({"metadata": metadata}, f, indent=4)
        return metadata

    def get_schema(self):
        """
        Returns the schema of the client.

        :return: The schema of the client.
        :rtype: build_client_schema.graphql.GraphQLSchema
        """
        return build_client_schema(self.get_sdl())

    def get_sdl(self):
        """
        Retrieves the Schema Definition Language (SDL) for the GraphQL API.

        Returns:
            str: The Schema Definition Language (SDL) for the GraphQL API.

        Raises:
            Exception: If there is an error executing the introspection query.

        Example:
            >>> sdl = obj.get_sdl()
        """
        introspection_query = """
            query IntrospectionQuery {
                __schema {
                    queryType {
                        name
                    }
                    mutationType {
                        name
                    }
                    subscriptionType {
                        name
                    }
                    types {
                        ...FullType
                    }
                    directives {
                        name
                        description
                        locations
                        args {
                            ...InputValue
                        }
                    }
                }
            }
    
            fragment FullType on __Type {
                kind
                name
                description
                fields(includeDeprecated: true) {
                    name
                    description
                    args {
                        ...InputValue
                    }
                    type {
                        ...TypeRef
                    }
                    isDeprecated
                    deprecationReason
                }
                inputFields {
                    ...InputValue
                }
                interfaces {
                    ...TypeRef
                }
                enumValues(includeDeprecated: true) {
                    name
                    description
                    isDeprecated
                    deprecationReason
                }
                possibleTypes {
                    ...TypeRef
                }
            }
    
            fragment InputValue on __InputValue {
                name
                description
                type {
                    ...TypeRef
                }
                defaultValue
            }
    
            fragment TypeRef on __Type {
                kind
                name
                ofType {
                    kind
                    name
                    ofType {
                        kind
                        name
                        ofType {
                            kind
                            name
                            # Continue nesting for more complex types if needed
                        }
                    }
                }
            }
            """
        return self.execute(introspection_query)

    def vectorize_result(self, min_features_dict=None):
        """
        Vectorizes the last query result using DictVectorizer.

        :return: self.vectorized_result, a dictionary with the same keys as the last query, but with the values
                 transformed into dense arrays using DictVectorizer.
        """
        self.vectorized_result = {}
        self.logging.debug(f'Vectorizing: {json.dumps(self.native_result, indent=2)}')
        for key in self.native_result:
            v = DictVectorizer(sparse=False)  # Set sparse=False for a dense array
            flatted_dict = flatten_nested_dicts(self.native_result[key])
            vectorized = vectorize_dicts(flatted_dict)
            self.vectorized_result[key] = v.fit_transform(vectorized)
            rows, num_features = self.vectorized_result[key].shape
            if min_features_dict is not None and min_features_dict.get(key) is not None and \
                    num_features < min_features_dict.get(key):
                vectorized = add_dummy_features(vectorized, min_features_dict.get(key),
                                                min_features_dict.get(key) - num_features)
                self.vectorized_result[key] = v.fit_transform(vectorized)
            self.logging.info(self.vectorized_result[key])
        return self.vectorized_result

    def clusters(self, n_clusters):
        """
        :param n_clusters: A dictionary containing the number of clusters for each key
        :return: A dictionary containing the clustered data for each key

        Performs clustering on the vectorized result using the KMedoids algorithm.
        Clusters the data for each key separately and returns a dictionary containing the clustered data for each key.

        Example usage:
            self.clusters({
                'key1': 3,
                'key2': 5,
                ...
            })
        """
        self.vectorize_result()
        clustered = {}
        for key in self.vectorized_result:
            kmedoids = KMedoids(n_clusters=n_clusters[key], random_state=42)
            kmedoids.fit(self.vectorized_result[key])
            cluster_labels = kmedoids.labels_
            clustered[key] = create_empty_arrays(cluster_labels.max() + 1)
            # Print the cluster assignments
            for i, cluster_label in enumerate(cluster_labels):
                clustered[key][cluster_label].append(self.native_result[key][i])
        return clustered

    def optimal_number_of_clusters(self, lower, upper):
        """
        Find the optimal number of clusters for each key in the vectorized result.

        :param lower: The lower bound of the range of cluster numbers to consider.
        :param upper: The upper bound of the range of cluster numbers to consider.
        :return: A dictionary containing the optimal number of clusters for each key in the vectorized result.
        """
        self.vectorize_result()
        clustered = {}
        for key in self.vectorized_result:
            costs = []
            for k in range(lower, upper + 1):
                kmedoids = KMedoids(n_clusters=min(k, len(self.vectorized_result[key]) - 1), random_state=42)
                kmedoids.fit(self.vectorized_result[key])
                costs.append(kmedoids.inertia_)
            clustered[key] = get_ordinal_of_smallest_number(compute_deltas(costs)) + 2
        return clustered

    def anomalies_training(self, output_dir=None, base64_encoded_data=False, database_output=False,
                           selection_set_hash=None):
        """
        Trains anomaly detection models and saves them.

        Args:
            output_dir (str, optional): The directory where the models will be saved. If not provided, the default directory will be used.
            base64_encoded_data (bool, optional): Indicates whether the models should be stored as base64-encoded data. Default is False.
            database_output (bool, optional): Indicates whether the models should be stored in a database. Default is False.
            selection_set_hash (str, optional): The hash value for this selection set. Default is an empty string.

        Returns:
            dict: A dictionary containing filenames/path of the saved models. If database_output is True and a MONGODB_CONNECTION_STRING environment variable is set, saves the model.

        Notes:
            - Requires scikit-learn library (version 0.22.2 or higher).
            - If base64_encoded_data ais True, the models will be returned as base64-encoded data in the dictionary.
            - The output_dir will be created if it doesn't exist.
            - The saved models are in pickle (.pkl) format.
            - If database_output is True, the models will be saved in a MongoDB collection named 'anomalyDetectionModels'.
            - The connection string for the MongoDB database should be provided as the MONGODB_CONNECTION_STRING environment variable.

        """
        if output_dir is not None:
            self.output_dir = output_dir
        self.vectorize_result()
        clf = IsolationForest(contamination=0.1, random_state=42)
        filenames = {"selectionSetHash": selection_set_hash, "operationName": self.operation_name}
        for key in self.vectorized_result:
            clf.fit(self.vectorized_result[key])
            temp_dir = tempfile.mkdtemp()
            filename = os.path.join(self.output_dir, temp_dir, key + '.pkl')
            if base64_encoded_data or database_output:
                filenames[key] = base64.b64encode(pickle.dumps(clf)).decode('utf-8')
            else:
                with open(filename, 'wb') as model_file:
                    pickle.dump(clf, model_file)
                    filenames[key] = filename
        if database_output and os.environ.get("MONGODB_CONNECTION_STRING") is not None:
            connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
            default_db_name = connection_string.split('/')[-1]
            client = MongoClient(connection_string)
            db = client[default_db_name]
            collection = db['anomalyDetectionModels']
            if selection_set_hash is not None:
                collection.update_one({"selectionSetHash": selection_set_hash}, {'$set': filenames}, upsert=True)
                client.close()
                return {"selectionSetHash": selection_set_hash}
            else:
                collection.update_one({"operationName": self.operation_name}, {'$set': filenames}, upsert=True)
                client.close()
                return {"operationName": self.operation_name}

        return filenames

    def anomalies(self, training_files=None, threshold=0, training_base64=None, selection_set_hash=None,
                  operation_name=None):
        """
        Args:
            training_files: A dictionary mapping keys to file paths for training files (default: None)
            threshold: The threshold value below which anomalies are considered (default: 0)
            training_base64: Base64 encoded training data (default: None)
            selection_set_hash: Hash value for selecting a specific set of training data (default: None)
            operation_name: Name of the operation for selecting training data (default: None)

        Returns:
            A dictionary containing anomalies found in the input data.
        """

        self.anomalies_result = {}
        # Initialize Isolation Forest
        trained_models = {}
        min_features = {}
        if selection_set_hash is not None:
            connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
            default_db_name = connection_string.split('/')[-1]
            client = MongoClient(connection_string)
            db = client[default_db_name]
            collection = db['anomalyDetectionModels']
            training_base64 = collection.find_one({"selectionSetHash": selection_set_hash})
            if training_base64 is not None and training_base64.get('selectionSetHash') is not None:
                self.logging.info('Loaded trained model from selectionSetHash')
            else:
                self.logging.info('Problem loading trained model from selectionSetHash. Will generate model from '
                                  'input dataset.')
            client.close()
        elif operation_name is not None:
            connection_string = os.environ.get("MONGODB_CONNECTION_STRING")
            default_db_name = connection_string.split('/')[-1]
            client = MongoClient(connection_string)
            db = client[default_db_name]
            collection = db['anomalyDetectionModels']
            training_base64 = collection.find_one({"operationName": operation_name})
            if training_base64 is not None and training_base64.get('operationName') is not None:
                self.logging.info('Loaded trained model from operationName')
            else:
                self.logging.info('Problem loading trained model from operationName. Will generate model from '
                                  'input dataset.')
            client.close()
        for key in self.vectorized_result:
            if training_files is not None:
                with open(training_files[key], 'rb') as model_file:
                    trained_models[key] = pickle.load(model_file)
                    min_features[key] = trained_models[key].n_features_in_
            elif training_base64 is not None:
                trained_models[key] = pickle.loads(base64.b64decode(training_base64[key]))
                min_features[key] = trained_models[key].n_features_in_
        self.vectorize_result(min_features)
        for key in self.vectorized_result:
            if trained_models.get(key) is None:
                trained_models[key] = IsolationForest(contamination=0.1, random_state=42)
                trained_models[key].fit(self.vectorized_result[key])
            scores = trained_models[key].decision_function(self.vectorized_result[key])
            merged = list(map(lambda x: add_score(self.native_result[key][x[0]], x[0], x[1]), enumerate(scores)))
            self.anomalies_result[key] = list(filter(lambda x: x['__score__'] < threshold, merged))
        return self.anomalies_result

    def convert_output_format(self, output_format):
        """
        Convert the output format of the result.

        :param output_format: The desired output format. Must be one of ExportFormat.FLAT, ExportFormat.DATAFRAME, ExportFormat.PARQUET, ExportFormat.CSV, ExportFormat.ARROW.
        :return: The converted result in the specified format.
        """
        self.result_format = output_format
        if output_format == ExportFormat.FLAT:
            self.result = self._transform_to_flatten()
        elif output_format in [ExportFormat.DATAFRAME, ExportFormat.PARQUET, ExportFormat.CSV]:
            self.result = self._transform_to_dataframe()
        elif output_format == ExportFormat.ARROW:
            self.result = self._transform_to_arrow()
        return self.result

    def get_extensions(self):
        """
        Returns the dict of extensions.

        Args:
            self: The object itself.

        Returns:
            A dictionary of extensions.
        """
        return self.extensions

    def get_data(self):
        """
        Method Name:
        get_data

        Description:
        This method retrieves the native result from the object.

        Parameters:
        self - The current object instance.

        Returns:
        The native result of the object.
        """
        return self.native_result

    def get_data_frame(self):
        """
        Method: get_data_frame

        Description:
        This method converts the native_result attribute to a Pandas DataFrame object and returns it.

        Parameters:
        - self: The instance of the class calling the method.

        Return Type:
        - Pandas DataFrame: A DataFrame object containing the data from the native_result attribute.

        Example Usage:
        df = instance.get_data_frame()

        """
        return pd.DataFrame(self.native_result)

    def upload_csv_folder(self, csv_folder, uri, if_exists='replace', casing=Casing.none):
        """
        Uploads a folder of CSV files to a specified URI.

        Args:
            csv_folder (str): The path to the folder containing the CSV files.
            uri (str): The destination database URI where the CSV files will be uploaded.
            if_exists (str, optional): The action to take if a table with the same name already exists at the destination URI. Default is 'replace'.
            casing (Casing, optional): The casing rule to apply to the column names. Defaults to Casing.none.

        Returns:
            The table names that were imported from the CSV files.
        """
        return import_tables(csv_folder=csv_folder, uri=uri, if_exists=if_exists, casing=casing, logging=self.logging)

    def write_to_file(self, output_dir=None, output_format=None):
        """
        Writes the result data to file(s) in the specified output format and directory.

        :param output_dir: The directory where the output file(s) will be written. If not provided, the current output directory is used.
        :param output_format: The format in which the output file(s) will be written. If not provided, the current output format is used.
        :return: A list of filenames corresponding to the output file(s) created.

        """
        if output_dir is not None:
            self.output_dir = output_dir
        if output_format is not None:
            self.convert_output_format(output_format)

        def filename_mapper(_output, _key):
            return {
                ExportFormat.NATURAL: self._get_file_path('result.json'),
                ExportFormat.FLAT: self._get_file_path(_key + '.json'),
                ExportFormat.PARQUET: self._get_file_path(_key + '.pq'),
                ExportFormat.CSV: self._get_file_path(_key + '.csv'),
                ExportFormat.ARROW: self._get_file_path(_key + '.arrow')
            }[_output]

        format_writers = {
            ExportFormat.NATURAL: self._write_result_as_file,
            ExportFormat.FLAT: self._write_result_as_file,
            ExportFormat.PARQUET: lambda _filename, data: data.to_parquet(_filename),
            ExportFormat.CSV: lambda _filename, data: data.to_csv(_filename, index=False),
            ExportFormat.ARROW: lambda _filename, data: pa.ipc.new_file(_filename, data.schema).write(
                data)
        }
        filenames = []
        if self.result_format == ExportFormat.NATURAL:
            filename = filename_mapper(self.result_format, '')
            format_writers[self.result_format](filename, self.native_result)
            return filename
        for key in self.result:
            filename = filename_mapper(self.result_format, key)
            filenames.append(filename)
            format_writers[self.result_format](filename, self.result[key])
        return filenames

    def track_pg_tables(self, tables, source="default", schema=None):
        """
        Args:
            tables: A list of table names to be tracked in Hasura.
            source: The name of the data source to be used for tracking the tables. Default value is "default".
            schema: The schema name of the tables. If provided, it will be used to qualify the table names.

        Returns:
            A dictionary containing the result of tracking each table. The keys are the table names and the values are the parsed JSON responses.

        """
        result = {}
        for table_name in tables:
            data = {
                "type": "pg_track_table",
                "args": {
                    "source": source,
                    "name": table_name,
                    "configuration": {
                        "apollo_federation_config": {
                            "enable": "v1"
                        }
                    }
                }
            }
            if schema is not None:
                data["args"]["schema"] = schema
            response = requests.post(
                self.uri.replace('graphql', 'metadata'),
                json=data,
                headers={
                    'x-hasura-admin-secret': self.admin_secret
                })
            result[table_name] = json.loads(response.text)
        requests.get(self.uri.replace('graphql', 'reload-schema'))
        self.get_metadata()
        return result

    def replace_metadata(self, metadata=None, allow_inconsistent_metadata=True, allow_warnings=True):
        """
        Args:
            metadata: A dictionary containing the new metadata to be replaced. If None, the existing metadata in the class instance will be used.
            allow_inconsistent_metadata: A boolean indicating whether to allow inconsistent metadata. Defaults to True.
            allow_warnings: A boolean indicating whether to allow warnings. Defaults to True.

        Returns:
            The response in JSON format received from the server after the metadata replacement.

        """
        data = {
            "type": "replace_metadata",
            "version": 2,
            "args": {
                "allow_inconsistent_metadata": allow_inconsistent_metadata,
                "allow_warnings": allow_warnings,
                "metadata": metadata or self.metadata
            }
        }

        response = requests.post(
            self.uri.replace('graphql', 'metadata'),
            json=data,
            headers={
                'x-hasura-admin-secret': self.admin_secret
            })
        result = response.json()
        self.get_metadata()
        return result

    def add_dbml_model_as_source(self, dbml_model_file, configuration, kind, output_file=None, customization=None):
        """
        Args:
            dbml_model_file: A string representing the file path of the DBML model file.
            configuration: A dictionary representing the Hasura data source configuration.
            kind: A string representing the kind of source to be added.
            output_file: (Optional) A string representing the file path where the result will be written. If not provided, the result will not be written to a file.
            customization: (Optional) A dictionary representing the customization options for the source.

        Returns:
            result: A dictionary representing the result of adding the DBML model as a source.

        Example usage:
            dbml_model_file = "/path/to/dbml_model_file.dbml"
            configuration = {
                "connection_info": {
                    "database_url": {
                        "from_env": "PG_DATABASE_URL1"
                    },
                    "isolation_level": "read-committed",
                    "use_prepared_statements": False
                }
            }
            kind = "database"
            output_file = "/path/to/output_file.json"
            customization = {
                "root_fields": {
                    "namespace": "myapp_",
                    "prefix": "prefix_",
                    "suffix": "_suffix"
                },
                "type_names": {
                    "prefix": "Type_",
                    "suffix": "_Type"
                }
            }

            result = add_dbml_model_as_source(dbml_model_file, configuration, kind, output_file, customization)
        """
        result = add_dbml(
            dbml_model_file,
            configuration=configuration,
            kind=kind,
            logging=self.logging,
            hasura_client=self,
            customization=customization
        )
        if output_file is not None:
            self._write_result_as_file(output_file, result)
        return result
