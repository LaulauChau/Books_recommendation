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


def add_reader(books: str, readers: str, booksread: str, rating_matrix: list[list[str]]) -> None:
    """Add a reader to the database."""
    
    with open(readers, "a+", encoding="utf-8") as readers_file, open(booksread, "a", encoding="utf-8") as booksread_file:
        reader_information = [
            get_username(readers),
            get_attribut(GENDER),
            get_attribut(AGE),
            get_attribut(READING_STYLE),
        ]
        
        reader_booksread = [reader_information[0]] + get_booksread(books)
        
        readers_file.write(",".join(reader_information) + "\n")
        booksread_file.write(",".join(reader_booksread) + "\n")
        
    ra.add_row(rating_matrix)
    
    
def display_reader(books: str, readers: str, booksread: str) -> None:
    """Display a reader in the database."""
    
    with open(readers, encoding="utf-8") as readers_file, open(booksread, encoding="utf-8") as booksread_file:
        readers_file_content = readers_file.read()
        booksread_file_content = booksread_file.read()
        
    while True:
        reader_username = input("Enter the reader's username: ").lower()
            
        if reader_username in readers_file_content.lower():
            break
        else:
            print("This reader is not in the database.")
            
    pattern = re.compile(f"{reader_username}.+", re.MULTILINE | re.IGNORECASE)
    reader_line = pattern.search(readers_file_content)[0].split(",")
    booksread_line = pattern.search(booksread_file_content)[0].split(",")
    
    print(f"Username: {reader_line[0]}")            
    print(f"Gender: {GENDER[reader_line[1]]}")            
    print(f"Age: {AGE[reader_line[2]]}")            
    print(f"Reading style: {READING_STYLE[reader_line[3]]}")
    
    print("Book(s) read:")
    books_name = get_books_name(books, booksread_line[1:])
    for name in books_name:
        print(name)
        
        
def reader_handling(books: str, readers: str, booksread: str, rating_matrix: list[list[int]], delete: bool = False) -> None:
    """
    Modify/Delete a reader in the database.
    Those functions were combine because they share the same principle.
    """
    
    with open(readers, encoding="utf-8") as readers_file, open(booksread, encoding="utf-8") as booksread_file:
        readers_file_content = readers_file.read()
        booksread_file_content = booksread_file.read()
        
        while True:
            reader_username = input("Enter the reader's username: ").lower()
            
            if reader_username in readers_file_content.lower():
                break
            else:
                print("This reader is not in the database.")
            
    pattern = re.compile(f"{reader_username}.+", re.MULTILINE | re.IGNORECASE)
    
    if delete:
        new_readers_file = pattern.sub("", readers_file_content)
        new_booksread_file = pattern.sub("", booksread_file_content)
        
        new_readers_file = "\n".join([x for x in new_readers_file.strip().split("\n") if x])
        new_booksread_file = "\n".join([x for x in new_booksread_file.strip().split("\n") if x])
        
        reader_index = get_reader_index(readers, reader_username)
        ra.delete_row(rating_matrix, reader_index)
    else:
        print("Generating a new profile:")
        reader_information = [
            get_username(reader, verification=False),
            get_attribut(GENDER),
            get_attribut(AGE),
            get_attribut(READING_STYLE),
        ]
        
        reader_booksread = [reader_information[0]] + get_booksread(books)
        
        new_readers_file = pattern.sub(",".join(reader_information), readers_file_content)
        new_booksread_file = pattern.sub(",".join(reader_booksread), booksread_file_content)
        
    with open(readers, "w", encoding="utf-8") as readers_file, open(booksread, "w", encoding="utf-8") as booksread_file:
        readers_file.write(new_readers_file)
        booksread_file.write(new_booksread_file)
        
  
""" ===== HELPERS FUNCTIONS ===== """


def get_username(readers: str, verification: bool = True) -> str:
    """Get the username of the reader to be added."""

    with open(readers, encoding="utf-8") as readers_file:
        readers_file_content = readers_file.read()

    while True:
        username = input("Enter the reader's username: ")

        if verification and username.lower() in readers_file_content.lower():
            print("Username already taken.")
        else:
            break

    return username 



def get_attribut(attribut: dict[str, str]) -> str:
    """Get the attribut of the reader to be added."""

    for key, value in attribut.items():
        print(f"{key} - {value}")

    while True:
        attribut_number = input("Enter the corresponding number: ")

        if attribut_number not in list(attribut.keys()):
            print("Incorrect number.")
        else:
            break

    return attribut_number


def get_booksread(books: str) -> list[str]:
    """Get the list of books read by the reader to be added."""

    books_read = []

    with open(books, encoding="utf-8") as books_file:
        books_names = dict(enumerate(books_file.readlines(), start=1))

    while True:
        for key, value in books_names.items():
            print(f"{key:>2} - {value.strip()}")

        book_index = input("Enter the number of the book you've read (0 to exit): ")

        if int(book_index) in list(books_names.keys()):
            books_read.append(book_index)
        elif book_index == "0":
            break
        else:
            print("Incorrect number.")

    return books_read


def get_books_name(books: str, books_read: list[str]) -> list[str]:
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