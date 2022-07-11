#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for reader manipulation."""


import re

from core import rating as ra


GENDER = {
    "1": "Man",
    "2": "Woman",
    "3": "Other",
}

AGE = {
    "1": "<= 18 years old",
    "2": "Between 18 years old and 25 years old",
    "3": "> 25 years old",
}

READING_STYLE = {
    "1": "Science fiction",
    "2": "Biography",
    "3": "Horror",
    "4": "Romance",
    "5": "Fable",
    "6": "History",
    "7": "Comedy",
}


def add_reader(books: str, readers: str, booksread: str, rating_matrix: list[list[str]], reader_information: list[list[str]]) -> None:
    """Add a reader to the database."""
    
    with open(readers, "a+", encoding="utf-8") as readers_file, open(booksread, "a", encoding="utf-8") as booksread_file:
        reader_profile, reader_booksread = reader_information

        readers_file.write(",".join(reader_profile) + "\n")
        booksread_file.write(",".join(reader_booksread) + "\n")
        
    ra.add_row(rating_matrix)
    
    
def display_reader(books: str, readers: str, booksread: str, reader_name: str) -> None:
    """Display a reader in the database."""
    
    with open(readers, encoding="utf-8") as readers_file, open(booksread, encoding="utf-8") as booksread_file:
        readers_file_content = readers_file.read()
        booksread_file_content = booksread_file.read()
            
    pattern = re.compile(f"{reader_name}.+", re.MULTILINE | re.IGNORECASE)
    reader_line = pattern.search(readers_file_content)[0].split(",")
    booksread_line = pattern.search(booksread_file_content)[0].split(",")
    
    reader_line = [reader_line[0]] + list(reader_line[1:])

    booksread_line = [
        int(element) for element in booksread_line[1:]
    ]
    
    reader_profile = f"Username : {reader_line[0]}\n" + f"Gender : {GENDER[reader_line[1]]}\n" + f"Age : {AGE[reader_line[2]]}\n" + f"Reading style : {READING_STYLE[reader_line[3]]}\n"
    books_name = get_books_names(books, booksread_line)
    reader_booksread = "\n".join(books_name)
    
    return reader_profile + reader_booksread
        
        
def reader_handling(books: str, readers: str, booksread: str, rating_matrix: list[list[int]], reader_name: str, reader_information: list[list[str]], delete: bool = False) -> None:
    """
    Modify/Delete a reader in the database.
    Those functions were combine because they share the same principle.
    """
    
    with open(readers, encoding="utf-8") as readers_file, open(booksread, encoding="utf-8") as booksread_file:
        readers_file_content = readers_file.read()
        booksread_file_content = booksread_file.read()
            
    pattern = re.compile(f"{reader_name}.+", re.MULTILINE | re.IGNORECASE)
    
    if delete:
        new_readers_file = pattern.sub("", readers_file_content)
        new_booksread_file = pattern.sub("", booksread_file_content)
        
        new_readers_file = "\n".join([x for x in new_readers_file.strip().split("\n") if x])
        new_booksread_file = "\n".join([x for x in new_booksread_file.strip().split("\n") if x])
        
        reader_index = get_reader_index(readers, reader_name)
        ra.delete_row(rating_matrix, reader_index)
    else:
        reader_profile, reader_booksread = reader_information
        
        new_readers_file = pattern.sub(",".join(reader_profile), readers_file_content)
        new_booksread_file = pattern.sub(",".join(reader_booksread), booksread_file_content)
        
    with open(readers, "w", encoding="utf-8") as readers_file, open(booksread, "w", encoding="utf-8") as booksread_file:
        readers_file.write(new_readers_file)
        booksread_file.write(new_booksread_file)
        
  
""" ===== HELPERS FUNCTIONS ===== """


def get_books_names(books: str, books_read: list[str]) -> list[str]:
    """Get the names of the books read by the reader."""

    with open(books, encoding="utf-8") as books_file:
        books_names = [name.strip() for index, name in enumerate(books_file.readlines(), start=1) if str(index) in books_read or index in books_read]
        
    return books_names
      
def get_reader_index(readers: str, reader_username: str) -> int:
    """Get the index of the reader."""
    
    with open(readers, encoding="utf-8") as readers_file:
        for index, name in enumerate(readers_file.readlines()):
            if reader_username.lower() in name.lower():
                return index
            
    return None