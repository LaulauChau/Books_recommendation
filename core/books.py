#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for book manipulation."""


import re

from core import rating


def display_books(books: str) -> None:
    """Displays all books in the deposit file."""
    
    with open(books, encoding="utf-8") as books_file:
        for index, name in enumerate(books_file.readlines(), start=1):
            print(f"{index:>2} - {name.strip()}")
            

def add_books(books: str, rating_matrix: list[list[int]]) -> None:
    """Add a book in the deposit file."""
    
    with open(books, "a+", encoding="utf-8") as books_file:
        books_file_content = books_file.read().lower()
        
        while True:
            book_name = input("Enter the name of the book: ")
            
            if book_name.lower() in books_file_content:
                print("Book already in the deposit.")
            else:
                books_file.write(book_name + "\n")


def book_handling(books: str, booksread: str, rating_matrix: list[list[int]], delete: bool = False) -> None:
    """
    Modify/Delete a book in the deposit.
    Those functions were combine because they share the same principle.
    """
    
    with open(books, encoding="utf-8") as books_file:
        books_name = books_file.readlines()
        
    while True:
        book_index = int(input("Enter the book number: ")) - 1
        
        if 0 <= book_index < len(books_name):
            break
        else:
            print("Incorrect number.")
            
    if delete:
        del books_name[book_index]
        delete_book(booksread, book_index)
        
        rating.column_handling(rating_matrix, book_index)
    else:
        books_name[book_index] = input("Enter the new name: ") + "\n"
    
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