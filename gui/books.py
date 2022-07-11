#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for book manipulation."""


import re

from core import rating


def display_books(books: str) -> None:
    """Displays all books in the deposit file."""
    
    with open(books, encoding="utf-8") as books_file:
        output = "".join(f"{index} - {name}" for index, name in enumerate(books_file.readlines(), start=1))
        
    return output
            

def add_books(books: str, rating_matrix: list[list[int]], book_name: str) -> None:
    """Add a book in the deposit file."""
    
    with open(books, "a", encoding="utf-8") as books_file:
        books_file.write(book_name + "\n")


def book_handling(books: str, booksread: str, rating_matrix: list[list[int]], book_name: list[str], delete: bool = False) -> None:
    """
    Modify/Delete a book in the deposit.
    Those functions were combine because they share the same principle.
    """
    
    with open(books, encoding="utf-8") as books_file:
        books_name = books_file.readlines()

    book_index = int(book_name[0])
            
    if delete:
        del books_name[book_index - 1]
        delete_book(booksread, book_index)
        
        rating.column_handling(rating_matrix, book_index)
    else:
        books_name[book_index - 1] = book_name[-1] + "\n"
    
    with open(books, "w", encoding="utf-8") as books_file:
        for book in books_name:
            books_file.write(book)
            
            
""" ===== HELPERS FUNCTIONS ===== """


def delete_book(booksread: str, book_index: int) -> None:
    """Removes the book from the list of read books."""
    
    with open(booksread, encoding="utf-8") as booksread_file:
        booksread_file_content = booksread_file.read()
        
    pattern = re.compile(f",{book_index}", re.MULTILINE)
    new_booksread_file = pattern.sub("", booksread_file_content)
    
    with open(booksread, "w", encoding="utf-8") as booksread_file:
        booksread_file.write(new_booksread_file)