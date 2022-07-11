#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for grading and recommending a book."""


import math
import re as regex

from core import readers as re


def grade_book(rating_matrix: list[list[int]], info: list[str]) -> None:
    """Allows a user to grade a book he has read."""
    
    reader_username, book, score = info

    rating_matrix[readers_name[reader_username]][int(book)] = score

    return rating_matrix
                

def recommend_book(books: str, booksread: str, rating_matrix: list[list[int]], user_1: str) -> str:
    """Recommend a book to a reader."""
    
    with open(booksread, encoding="utf-8") as booksread_file:
        booksread_file_content = booksread_file.readlines()
    
    similarity_matrix = similarities_matrix(rating_matrix)
    
    for index, line in enumerate(booksread_file_content):
        if user_1.lower() in line.lower():
            similar = most_similar(similarity_matrix[index])
            user_1 = line.strip().split(",")[1:]
            break

    user_2 = booksread_file_content[similar].strip().split(",")[1:]
    
    user_1 = [int(x) for x in user_1]
    user_2 = [int(x) for x in user_2]
    
    books_recommended = list(set(user_1).symmetric_difference(set(user_2)))
    books_recommended = re.get_books_name(books, books_recommended)
    
    return "\n".join(books_recommended)
        
        
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

    return index


def get_matrix(matrix: str) -> None:
    """Extract a matrix from its file."""
    
    with open(matrix) as matrix_file:
        rating_matrix = [
            [int(rating) for rating in row.split()] for row in matrix_file.readlines()
        ]
        
    return rating_matrix