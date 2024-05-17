from pymongo import MongoClient
import json


def export_schema(conn_str,db_name):
    """
    Export database schema include indexes and options.

    Args:
        conn_str (string): connection string.
        db_name (string): data base name.

    Returns:
        json file: save the schema to a schema.json file.
    """

    # Connect to MongoDB
    client = MongoClient(conn_str)

    # Select the database to export the schema from
    db = client[db_name]

    # Get the schema of the database including indexes
    schema = {}
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        index_info = collection.index_information()
        if '_id_' in index_info:
            # Remove the default _id_ index to reduce schema size
            del index_info['_id_']
        schema[collection_name] = {
            'indexes': index_info,
            'options': collection.options(),
        }

    # Save the schema to a file
    with open('schema.json', 'w') as f:
        f.write(json.dumps(schema))


def import_schema(conn_str,db_name):
    """
    Import database schema include indexes and options.

    Args:
        conn_str (string): connection string.
        db_name (string): data base name.
    """
    # Connect to MongoDB
    client = MongoClient(conn_str)

    # Select the database to import the schema to
    db = client[db_name]

    # Load the schema from a file
    with open('schema.json', 'r') as f:
        schema = json.load(f)

    # Create each collection with indexes and options
    for collection_name, info in schema.items():
        collection = db.create_collection(collection_name, **info['options'])
        indexes = info['indexes']
        for index in indexes:
            collection.create_index(**index)

if __name__ == "__main__":
    export_schema("mongodb://eatng:%40TczbhNCS5XaQKY%26@172.29.5.205:27017/sessiondb?authSource=sessiondb&readPreference=primary&directConnection=true&ssl=false","sessiondb")