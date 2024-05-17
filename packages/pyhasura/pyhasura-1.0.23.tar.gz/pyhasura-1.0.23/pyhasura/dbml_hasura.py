from pydbml import PyDBML
from pathlib import Path
import camelcaser as cc
from pluralizer import Pluralizer

pluralizer = Pluralizer()


def add_dbml(dbml_file, kind, configuration, logging, hasura_client, customization):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
    parsed = PyDBML(Path(dbml_file))
    source = {
        "name": cc.make_camel_case(Path('global-retail-sales.dbml').stem),
        "kind": kind,
        "tables": [],
        "configuration": configuration,
        "customization": customization
    }

    rel_types = {
        "<": ("array", "object"),
        ">": ("object", "array"),
        "<>": ("array", "array"),
        "-": ("object", "object")
    }

    def create_table_metadata(dbml_table):
        return {
            "table": {
                "name": dbml_table.name,
                "schema": dbml_table.schema
            },
            "configuration": {
                "column_config": {},
                "custom_column_names": {},
                "custom_name": cc.make_camel_case(dbml_table.name),
                "custom_root_fields": {},
                "comment": dbml_table.note.text
            },
            "object_relationships": [],
            "array_relationships": []
        }

    def create_column_metadata(table_metadata, dbml_column):
        table_metadata["configuration"]["column_config"][dbml_column.name] = {
            "custom_name": cc.make_lower_camel_case(dbml_column.name),
            "comment": dbml_column.note.text
        }
        table_metadata["configuration"]["custom_column_names"][dbml_column.name] = cc.make_lower_camel_case(
            dbml_column.name)
        return table_metadata

    def create_relationship_metadata(dbml_ref, reverse=False):
        column_mapping = {}
        if reverse:
            for index, dbml_column in enumerate(dbml_ref.col2):
                column_mapping[dbml_column.name] = dbml_ref.col1[index].name
        else:
            for index, dbml_column in enumerate(dbml_ref.col1):
                column_mapping[dbml_column.name] = dbml_ref.col2[index].name
        return {
            "name": dbml_ref.name or cc.make_lower_camel_case(
                pluralizer.plural(dbml_ref.table1.name if reverse else dbml_ref.table2.name)),
            "comment": dbml_ref.comment,
            "using": {
                "manual_configuration": {
                    "column_mapping": column_mapping,
                    "insertion_order": None,
                    "remote_table": {
                        "name": dbml_ref.table1.name if reverse else dbml_ref.table2.name,
                        "schema": dbml_ref.table1.schema if reverse else dbml_ref.table2.schema,
                    }
                }
            }
        }

    for table in parsed.tables:
        new_table = create_table_metadata(table)
        for column in table.columns:
            create_column_metadata(new_table, column)
        source["tables"].append(new_table)
    for ref in parsed.refs:
        forward_rel_type = str(rel_types[ref.type][0])
        reverse_rel_type = str(rel_types[ref.type][1])
        forward_rel = create_relationship_metadata(ref)
        reverse_rel = create_relationship_metadata(ref, reverse=True)
        forward_table = [table for table in source["tables"] if table["table"]["name"] == ref.table1.name][0]
        forward_table[f"{forward_rel_type}_relationships"].append(forward_rel)
        reverse_table = [table for table in source["tables"] if table["table"]["name"] == ref.table2.name][0]
        reverse_table[f"{reverse_rel_type}_relationships"].append(reverse_rel)

    metadata = hasura_client.get_metadata()
    metadata["sources"].append(source)

    return metadata
