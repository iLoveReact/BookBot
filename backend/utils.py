import os
import pathlib
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter


def embed_a_book(book_path: str) -> str:
    # Returns path to the book index
    indexes_path = str(pathlib.Path().resolve()).replace("\\", "/") + "/Indexes"
    available_indexes = [index for index in os.listdir(indexes_path)]
    searched_path = book_path.split("/")[-1] + "_index"

    if searched_path not in available_indexes:
        loader = PyPDFLoader(book_path)
        text_splitter = CharacterTextSplitter(chunk_size=400, chunk_overlap=50)
        pages = loader.load_and_split(text_splitter=text_splitter)
        embeddings = OpenAIEmbeddings()

        db = FAISS.from_documents(pages, embeddings)
        db.save_local(indexes_path + "/" + searched_path)

    return indexes_path + "/" + searched_path