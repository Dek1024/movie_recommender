from pymongo import MongoClient
from streamlit import _RerunData, _RerunException
from streamlit.source_util import get_pages
from bson import ObjectId

def switch_page(page_name: str):

    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")
    
    page_name = standardize_name(page_name)

    pages = get_pages("landing_page.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise _RerunException(
                _RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")

#A function to get all the unique genre from the database
def get_unique_genre():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['moviedatabase']
    movie_collection = db['movies_database']
    unique_genre= []
    for document in movie_collection.find({}):
        genre_string = document["Genre"]
        genre_list = genre_string.split(",")
        for genre in genre_list:
            if genre in unique_genre:
                unique_genre.append(genre)
    return unique_genre

#A method to convert strings from pandas dataframe to ObjectId
def str_to_bson_object_id(input_dict: dict):
    list_updated = []
    for strings in input_dict["_id"]:
        list_updated.append(ObjectId(strings))
    input_dict["_id"] = list_updated
    return input_dict