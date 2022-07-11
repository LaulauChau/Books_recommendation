#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for executing the program in CLI."""


from core import books as b
from core import rating as ra
from core import readers as re


def action_error(*args) -> None:
    """Error when the user input an action not in the menu."""

    print("No such action")
    

def main_menu(books: str, readers: str, booksread: str, rating_matrix: list[list[int]]) -> None:
    """Main menu."""
    
    print("Choose between:")
    print("1 - Reader handling")
    print("2 - Book handling")
    print("3 - Recommendation")
    choice = int(input("Enter the corresponding number: "))
    
    menu = {1: readers_menu, 2: books_menu, 3: recommendation_menu}
    
    action = menu.get(choice, action_error)
    action(books, readers, booksread, rating_matrix)
    
    
def readers_menu(books: str, readers: str, booksread: str, rating_matrix: list[list[int]]) -> None:
    """Reader handling."""
    
    print("Choose between:")
    print("1 - Add a reader")
    print("2 - Display a reader")
    print("3 - Modify a reader")
    print("4 - Delete a reader")
    choice = int(input("Enter the corresponding number: "))
    
    if choice == 1:
        re.add_reader(books, readers, booksread, rating_matrix)
    elif choice == 2:
        re.display_reader(books, readers, booksread)
    elif choice == 3:
        re.reader_handling(books, readers, booksread, rating_matrix, delete=False)
    elif choice == 4:
        re.reader_handling(books, readers, booksread, rating_matrix, delete=True)
    else:
        action_error(books)
        
        
def books_menu(books: str, readers: str, booksread: str, rating_matrix: list[list[int]]) -> None:
    """Book handling."""
    
    print("Choose between:")
    print("1 - Display books")
    print("2 - Add a book")
    print("3 - Modify a book")
    print("4 - Delete a book")
    choice = int(input("Enter the corresponding number: "))
    
    if choice == 1:
        b.display_books(books)
    elif choice == 2:
        b.add_books(books, rating_matrix)
    elif choice == 3:
        b.book_handling(books, booksread, rating_matrix, delete=False)
    elif choice == 4:
        b.book_handling(books, booksread, rating_matrix, delete=True)
    else:
        action_error(books)
        
        
def recommendation_menu(books: str, readers: str, booksread: str, rating_matrix: list[list[int]]) -> None:
    """Recommendation menu."""
    
    print("Choose between:")
    print("1 - Grade a book")
    print("2 - Recommend a book")
    choice = int(input("Enter the corresponding number: "))
    
    if choice == 1:
        ra.grade_book(books, readers, booksread, rating_matrix)
    elif choice == 2:
        ra.recommend_book(books, booksread, rating_matrix)
    else:
        action_error(books)
