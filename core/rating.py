#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for grading and recommending a book."""


import math
import re

from core import readers


def grade_book(books: str, readers: str, booksread: str, rating_matrix: list[list[int]], reader_username: str = None) -> None:
    """Allows a user to grade a book he has read."""
    
    with open(books, encoding="utf-8") as books_file, open(readers, encoding="utf-8") as readers_file, open(booksread, encoding="utf-8") as booksread_file:
        books_name = {name.strip().lower(): str(index) for index, name in enumerate(books_file.readlines())}
        readers_name = {name.split(",")[0].lower(): index for index, name in enumerate(readers_file.readlines())}
        booksread_file_content = booksread_file.read().lower()
        
        if not reader_username:
            while True:
                reader_username = input("Enter the reader's username: ")
                
                if reader_username not in list(readers_name.keys()):
                    print("Reader not in the database.")
                else:
                    break
                
        while True:
            book = input("Enter the name of the book: ").lower()
            
            if book not in list(books_name.keys()):
                print("Book not in the database.")
            else:
                book = books_name[book]
                
                if book not in re.search(f"{reader_username}.+", booksread_file_content)[0]:
                    print("You have not read that book.")
                else:
                    break
                
    while True:
        score = int(input("Enter a score between 1 and 5: "))
            
        if 1 <= score <= 5:
            break
        else:
            print("Incorrect number.")
            
    rating_matrix[readers_name[reader_username]][int(book)] = score
    
    return rating_matrix
                

def recommend_book(books: str, booksread: str, rating_matrix: list[list[int]]) -> str:
    """Recommend a book to a reader."""
    
    with open(booksread, encoding="utf-8") as booksread_file:
        booksread_file_content = booksread_file.readlines()
    
    similarity_matrix = similarities_matrix(rating_matrix)
    user_1 = input("Enter the reader's username: ").lower()
    
    for index, line in enumerate(booksread_file_content):
        if user_1 in line:
            similar = most_similar(similarity_matrix[index])
            user_1 = line.strip().split(",")[1:]
        
    user_2 = booksread_file_content[similar].strip().split(",")[1:]
    
    user_1 = [int(x) for x in user_1]
    user_2 = [int(x) for x in user_2]
    
    books_recommended = set(user_2) - set(user_1)
    books_recommend = readers.get_books_name(books, books_recommended)
    
    print("Book(s) recommended:")
    for book in books_recommend:
        print(book)
        
        
""" ===== HELPERS FUNCTIONS ===== """


def init_matix(books: str, readers: str) -> list[list[int]]:
    """Create the rating matrix."""
    
    with open(books) as books_file, open(readers) as readers_file:
        nb_books = len(books_file.readlines())
        nb_readers = len(readers_file.readlines())
        
    return [[0 for _ in range(nb_books)] for _ in range(nb_readers)]


def write_matrix(matrix: str, rating_matrix: list[list[int]]):
    """Write the matrix in its file."""
    
    with open(matrix, "w") as matrix_file:
        for row in rating_matrix:
            matrix_file.write(" ".join(row) + "\n")
            
            
def add_row(rating_matrix: list[list[int]]) -> None:
    """Add a row after adding a reader to the deposit file."""
    
    nb_books = len(rating_matrix[0])
    rating_matrix.append([0 for _ in range(nb_books)])
    

def delete_row(rating_matrix: list[list[int]], user_index: int) -> None:
    """Delete a row after deleting a reader in the deposit file."""
    
    del rating_matrix[user_index]
    
    
def column_handling(rating_matrix: list[list[int]], book_index: int, delete: bool = False) -> None:
    """Add/Delete a column after handling a book in the deposit file."""
    
    for i in range(len(rating_matrix)):
        if delete:
            del rating_matrix[i][book_index - 1]
        else:
            rating_matrix[i].append(0)


def compute(reader_1: list[int], reader_2: list[int]) -> float:
    """Compute the similarities between two readers."""

    numerator = sum((a * b) for a, b in zip(reader_1, reader_2))
    denominator = math.sqrt(sum((a * a) for a in reader_1)) * math.sqrt(sum((b * b) for b in reader_2))

    return round(numerator / denominator, 2)


def similarities_matrix(rating_matrix: list[list[int]]) -> list[list[float]]:
    """Compute the similarites matrix."""
    
    similarity_matrix = []
    
    for reader_1 in rating_matrix:
        temp = []
        
        for reader_2 in rating_matrix:
            if reader_1 == reader_2:
                temp.append(1.0)
            else:
                temp.append(compute(reader_1, reader_2))
        
        similarity_matrix.append(temp)
        
    return similarity_matrix


def most_similar(row: list[float]) -> int:
    """Find the most similar reader."""
    
    maximum, index = 0, 0

    for i, j in enumerate(row):
        if j != 1 and j > maximum:
            maximum, index = j, i

    return 