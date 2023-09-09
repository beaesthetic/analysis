import pandas as pd
import pymongo


def export_mongo_collection(connection_str: str, db: str, collection: str, csv_target_file: str) -> str:
    client = pymongo.MongoClient(connection_str)
    db_ref = client[db]
    collection_ref = db_ref[collection]
    cursor = collection_ref.find({})  # find all
    df = pd.DataFrame(list(cursor))
    df.to_csv(csv_target_file, index=False)
    client.close()

    return csv_target_file
