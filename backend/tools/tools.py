from typing import List
import os
from langchain_openai import ChatOpenAI
import pathlib


def get_books_pdf_paths(name: str = "") -> List[str]:
    """Provides all book paths. Can be used to retrieve a path of specific book"""
    abs_path = str(pathlib.Path().resolve()).replace("\\", "/") + "/books"
    book_paths = [abs_path + "/" + book for book in os.listdir(abs_path)]

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    book_path = llm.invoke(f"Retrieve path to the book of a {name}, From this list {str(book_paths)}. Answer with only path")

    return book_path
