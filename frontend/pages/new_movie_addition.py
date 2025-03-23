import streamlit as st
#from .. import front_end_modules
from pymongo import MongoClient
import os
import requests

def switch_page(page_name: str):
    from streamlit import _RerunData, _RerunException
    from streamlit.source_util import get_pages

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

def get_unique_genre_using_set():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['moviedatabase']
    movie_collection = db['movies_database']
    unique_genre= []
    for document in movie_collection.find({}):
        genre_string = document["Genre"]
        genre_list = genre_string.split(",")
        for genre in genre_list:
            unique_genre.append(genre)
    unique_genre = set(unique_genre)
    return unique_genre

st.title("Adding Movie to Collection")
Title = st.text_input("Title")
Year = st.text_input("Year")
Cast = st.text_input("Cast")

genre_list = get_unique_genre_using_set()
selected_genre = st.multiselect("Preferred_genre",genre_list,max_selections=5)
Genre = ""
for genre in selected_genre:
    if len(Genre) == 0:
        Genre = genre
    else:
        Genre = Genre + "," +genre

Rating = st.text_input("Rating")

if st.button("Confirm movie addition ?"):
    headers = {"Authorization": f"Bearer {os.environ["token"]}"}
    url = "http://127.0.0.1:8000/add_movie"
    data = {"Title":Title,"Genre":Genre,"Actors":Cast,"Year":Year,"Rating":Rating}
    response = requests.put(url,json=data,headers=headers)
    response = response.json()
    st.write(response)

if st.button("Homepage"):
    st.switch_page("pages/home_page.py")

if st.button("Logout"):
     os.environ["token"] = "logged_out"
     st.switch_page("landing_page.py")