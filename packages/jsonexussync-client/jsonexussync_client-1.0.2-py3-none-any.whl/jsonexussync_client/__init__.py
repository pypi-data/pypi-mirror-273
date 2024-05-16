import asyncio
import websockets
import json

class JSONexusSyncClient:
    def __init__(self, config):
        self.server_uri = config['server_uri']
        if 'api_key' not in config:
            pass
        else:
            self.api_key = config['api_key']

    async def send_request(self, method, **kwargs):
        async with websockets.connect(self.server_uri) as websocket:
            request_data = {'api_key': self.api_key, 'method': method, **kwargs}
            await websocket.send(json.dumps(request_data))
            response = await websocket.recv()
            return json.loads(response)
    async def generate_api(self, name, db):
        async with websockets.connect(self.server_uri) as websocket:
            request_data = {'method': 'generate_api_key', 'name': name, 'db': db}
            await websocket.send(json.dumps(request_data))
            response = await websocket.recv()
            return json.loads(response)
    async def create_dbs(self, db_name):
        async with websockets.connect(self.server_uri) as websocket:
            request_data = {'method': 'create_db', 'db': db_name}
            await websocket.send(json.dumps(request_data))
            response = await websocket.recv()
            return json.loads(response)
    async def insert_data(self, collection_name, data):
        return await self.send_request('insert', collection_name=collection_name, data=data)

    async def find_data(self, collection_name, query):
        return await self.send_request('find', collection_name=collection_name, query=query)
    
    async def match_data(self, collection_name, query):
        return await self.send_request('match', collection_name=collection_name, query=query)
    
    async def update_data(self, collection_name, query, update_fields):
        return await self.send_request('update', collection_name=collection_name, query=query, update_fields=update_fields)

    async def delete_data(self, collection_name, query):
        return await self.send_request('delete', collection_name=collection_name, query=query)
    
    async def create_collection(self, collection_name):
        return await self.send_request('create_collection', collection_name=collection_name)
    
    async def get_dbs(self):
        return await self.send_request('get_dbs')
    
    async def create_db(self, db_name):
        return await self.create_dbs(db_name=db_name)
    
    async def generate_api_key(self,name, db):
        return await self.generate_api(name=name, db=db)
