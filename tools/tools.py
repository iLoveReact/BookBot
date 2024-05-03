from typing import List
import os
import pathlib

from langchain_core.tools import tool


def get_books_pdf_paths(name: str = "") -> List[str]:
    """Provides all book paths. Can be used to retrieve a path of specific book, does't take any arguments"""
    abs_path = str(pathlib.Path().resolve()).replace("\\", "/") + "/books"
    book_paths = [abs_path + "/" + book for book in os.listdir(abs_path)]

    return book_paths
