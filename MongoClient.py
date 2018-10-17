import logging

from pymongo import MongoClient

from Constants import *

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def connect_mongo_and_return_collection():
    client = MongoClient(MONGO_URL)

    if client is None:
        logging.error("Something went wrong while creating the MongoDB client...")
        return

    logging.info("The MongoDB client has been successfully connected to -> " + MONGO_URL)

    try:
        db = client.test
        return db.testCollection
    except:
        print("Something went wrong while fetching the table from the MongoDB client...")


def insert_document(document):
    collection = connect_mongo_and_return_collection()
    # testEntry = dict()
    # testEntry["title"] = "ashish"
    # testEntry["t2"] = "sinha"
    print("In progress data -> " + str(document))
    result = collection.insert(document)

    if result is None:
        logging.error("Couldn't insert the document to the database...")
        print("Couldn't insert the document to the database")
    else:
        logging.info("Successfully inserted the document to the database with key -> " + str(result))
        print("Inserted the document to the database with key -> " + str(result))

