from typing import List
import os

def get_books_pdf_paths() -> List[str]:
    """Provides all book paths. Can be used to retrieve a path of specific book"""
    book_paths = ["book/" + book for book in os.listdir("../books")]

    return book_paths
