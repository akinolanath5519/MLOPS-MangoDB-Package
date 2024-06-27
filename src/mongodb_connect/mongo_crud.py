import os
import pandas as pd
from pymongo import MongoClient
import json
from ensure import ensure_annotations
from typing import Any, Union


class MongoOperation:
    __collection = None
    __database = None
    
    def __init__(self, client_url: str, database_name: str, collection_name: str = None):
        self.client_url = client_url
        self.database_name = database_name
        self.collection_name = collection_name

    def create_mongo_client(self) -> MongoClient:
        client = MongoClient(self.client_url)
        return client
    
    def create_database(self) -> Any:
        if MongoOperation.__database is None:
            client = self.create_mongo_client()
            self.database = client[self.database_name]
            MongoOperation.__database = self.database
        return self.database
    
    def create_collection(self, collection_name: str = None) -> Any:
        if collection_name is None:
            collection_name = self.collection_name
        
        if MongoOperation.__collection is None or MongoOperation.__collection != collection_name:
            database = self.create_database()
            self.collection = database[collection_name]
            MongoOperation.__collection = self.collection
        return self.collection
    
    def insert_record(self, record: Union[dict, list], collection_name: str) -> None:
        collection = self.create_collection(collection_name)
        
        if isinstance(record, list):
            for data in record:
                if not isinstance(data, dict):
                    raise TypeError("Each record must be a dict")
            collection.insert_many(record)
        elif isinstance(record, dict):
            collection.insert_one(record)
        else:
            raise TypeError("Record must be a dict or a list of dicts")
    
    def bulk_insert(self, datafile: str, collection_name: str = None) -> None:
        if datafile.endswith('.csv'):
            dataframe = pd.read_csv(datafile, encoding='utf-8')
        elif datafile.endswith(".xlsx"):
            dataframe = pd.read_excel(datafile)
        else:
            raise ValueError("File must be a CSV or Excel file")
        
        datajson = json.loads(dataframe.to_json(orient='records'))
        collection = self.create_collection(collection_name)
        collection.insert_many(datajson)
