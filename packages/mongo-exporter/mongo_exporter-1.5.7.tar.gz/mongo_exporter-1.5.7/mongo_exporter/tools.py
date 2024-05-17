from pymongo import MongoClient,errors
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
        
        try:
            options = db.command("collstats", collection_name).get('options', {})
        except errors.OperationFailure as e:
            print(f"Could not retrieve options for collection '{collection_name}': {e}")
            options = {}
            
        schema[collection_name] = {
            'indexes': index_info,
            'options': options,#collection.options(),
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
        try:
            # Create collection with options
            collection = db.create_collection(collection_name, **info['options'])
            print(f"Collection '{collection_name}' created successfully.")
        except errors.CollectionInvalid:
            collection = db.get_collection(collection_name)
            print(f"Collection '{collection_name}' already exists.")
        
        collection = db[collection_name]
        
        for index_name, index_info in info['indexes'].items():
            index_keys = index_keys = [(field, int(specifier) if specifier in [1, -1] else specifier) for field, specifier in index_info['key']]
            #[tuple(key) for key in index_info['key']]

            for field, specifier in index_keys:
                if specifier not in [1, -1, '2d', '2dsphere', 'text', 'hashed']:
                    raise ValueError(f"Invalid index specifier '{specifier}' for field '{field}' in index '{index_name}' of collection '{collection_name}'.")
            
            index_options = {k: v for k, v in index_info.items() if k not in ['key', 'ns', 'v']}
            try:
                print(f"Index '{index_name}' keys '{index_keys}'")
                collection.create_index(index_keys, name=index_name, **index_options)
                print(f"Index '{index_name}' created successfully in collection '{collection_name}'.")
            except errors.OperationFailure as e:
                print(f"Error creating index '{index_name}' in collection '{collection_name}': {e}")

if __name__ == "__main__":
    export_schema("mongodb://eatng:%40TczbhNCS5XaQKY%26@172.29.5.205:27017/sessiondb?authSource=sessiondb&readPreference=primary&directConnection=true&ssl=false","sessiondb")