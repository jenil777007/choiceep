import logging

from pymongo import MongoClient, ReturnDocument

from Constants import *

logging.basicConfig(format='%(asctime)s - %(message)s')


def connect_mongo_and_return_collection():
    client = MongoClient(MONGO_URL)

    if client is None:
        logging.error("Something went wrong while creating the MongoDB client...")
        return

    logging.info("The MongoDB client has been successfully connected to -> " + MONGO_URL)

    try:
        db = client[MONGO_DB_NAME]
        return db[MONGO_DB_COLLECTION]
    except:
        print("Something went wrong while fetching the table from the MongoDB client...")


def insert_document_into_db(document):
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


def find_document_in_db(document):
    collection = connect_mongo_and_return_collection()
    logging.info("Finding this document in db -> " + str(document))
    result = collection.find(document)

    if result is None:
        logging.error("Couldn't find the document in to the database...")

    return result


def update_timeStamp_of_document_in_db(document):
    collection = connect_mongo_and_return_collection()
    logging.info("Updating this document in db -> " + str(document))
    collection.find_one_and_update({"_id": document['_id']}, {"$set": {"timeStamp": document['timeStamp']}},
                                   return_document=ReturnDocument.AFTER)
