from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://reynolkw:yOUm8GL158U4uqv6@cluster0.lrbmqco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
dbclient = MongoClient(uri, server_api=ServerApi('1'))