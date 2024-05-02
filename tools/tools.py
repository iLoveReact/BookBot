from typing import List
import os

from langchain_core.tools import tool


def get_books_pdf_paths(name: str = "") -> List[str]:
    """Provides all book paths. Can be used to retrieve a path of specific book, does't take any arguments"""
    book_paths = ["books/" + book for book in os.listdir("C:/Users/Asus/Desktop/books_app/books")]

    return book_paths
