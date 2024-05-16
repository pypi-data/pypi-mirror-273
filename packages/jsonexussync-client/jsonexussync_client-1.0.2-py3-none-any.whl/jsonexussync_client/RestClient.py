import requests
import json


class JSONexusSyncClient:
    def __init__(self, config):
        self.api_key = config['api_key']
        self.server_uri = config['server_uri']
        self.headers = {
            "Content-Type": "application/json",
            "X-API-KEY": self.api_key
            }

    def find(self, collection_name, query):
        _query = {collection_name: {"find":query}}
        return requests.post(self.server_uri, json=_query, headers=self.headers).json()

    def find_one(self, collection_name, query):
        _query = {collection_name: {"find_one":query}}
        return requests.post(self.server_uri, json=_query, headers=self.headers).json()
    
    def insert(self, collection_name, data):
        _query = {collection_name: {"insert":data}}
        return requests.post(self.server_uri, json=_query, headers=self.headers).json()
    
    def delete(self, collection_name, query):
        _query = {collection_name: {"delete":query}}
        return requests.post(self.server_uri, json=_query, headers=self.headers).json()
    
    def update(self, collection_name, query, update_fields):
        _query = {collection_name: {"update":[query, update_fields]}}
        return requests.post(self.server_uri, json=_query, headers=self.headers).json()
    
    def count(self, collection_name):
        _query = {collection_name: {"count":collection_name}}
        return requests.post(self.server_uri, json=_query, headers=self.headers).json()
    
    def get_collection(self, collection_name):
        _query = {collection_name: {"get_collection":collection_name}}
        return requests.post(self.server_uri, json=_query, headers=self.headers).json()
    
    def create_collection(self, collection_name):
        _query = {collection_name: {"create_collection":{"name":collection_name}}}
        return requests.post(self.server_uri, json=_query, headers=self.headers).json()
