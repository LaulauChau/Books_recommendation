#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module for executing the program in GUI."""


import PySimpleGUI as sg

from gui import books as b
from gui import rating as ra
from gui import readers as re


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

gender = "\n".join(f"{key} - {value}" for key, value in GENDER.items())
age = "\n".join(f"{key} - {value}" for key, value in AGE.items())
reading_style = "\n".join(f"{key} - {value}" for key, value in READING_STYLE.items())


def block_focus(window) -> None:
    for key in window.key_dict:
        element = window[key]

        if isinstance(element, sg.Button):
            element.block_focus()
            
            
def menu() -> None:
    layout = [
        [sg.Text("Choose a functionnality"),],
        [
            sg.Frame("Readers handling",
                     [
                         [
                             sg.Button("Add a reader"), sg.Button("Display a reader"), sg.Button("Modify a reader"), sg.Button("Delete a reader"),
                         ],
                     ])
        ],
        [
            sg.Frame("Books handling",
                     [
                         [
                             sg.Button("Display book"), sg.Button("Add a book"), sg.Button("Modify a book"), sg.Button("Delete a book"),
                         ],
                     ])
        ],
        [
            sg.Frame("Recommendation",
                     [
                         [
                             sg.Button("Grade a book"), sg.Button("Recommend a book"),
                         ],
                     ])
        ],
        [sg.HSeparator()],
        [sg.Button("Quit")],
    ]
    
    return sg.Window("Main menu", layout, finalize=True)


def add_reader(books: str, readers: str, booksread: str, rating_matrix: list[list[int]]) -> None:
    layout = [
        [sg.Text("Enter the reader's username: "), sg.In(key="-NAME-")],
        [sg.Text(gender)],
        [sg.Text("Enter the corresponding number: "), sg.In(key="-GENDER-")],
        [sg.Text(age)],
        [sg.Text("Enter the corresponding number: "), sg.In(key="-AGE-")],
        [sg.Text(reading_style)],
        [sg.Text("Enter the corresponding number: "), sg.In(key="-READING_STYLE-")],
        [sg.Text(b.display_books(books))],
        [sg.Text("Enter the number of the books you've read, separated by comas (e.g. 5,7,10): "), sg.In(key="-BOOKS_READ-")],
        [sg.Button("Add")]
    ]
    
    window = sg.Window("Add reader", layout, finalize=True, modal=True)
    block_focus(window)
    
    event, values = window.read()
    
    reader_profile = [values["-NAME-"], values["-GENDER-"], values["-AGE-"], values["-READING_STYLE-"]]
    reader_booksread = [values["-NAME-"]] + values["-BOOKS_READ-"].split(",")
    
    if event == "Add":
        re.add_reader(books, readers, booksread, rating_matrix, reader_information=[reader_profile, reader_booksread])
    
    window.close()


def display_reader(books: str, readers: str, booksread: str) -> None:
    layout = [
        [sg.Text("Enter the reader's username: ")],
        [sg.In(key="-NAME-")],
        [sg.Button("Display")],
    ]
    
    window = sg.Window("Display reader", layout, finalize=True, modal=True)
    block_focus(window)
    
    event, values = window.read()
    
    if event == "Display":
        sg.Popup(re.display_reader(books, readers, booksread, reader_name=values["-NAME-"]))
        
    window.close()
    

def modify_reader(books, readers: str, booksread: str, rating_matrix: list[list[int]]) -> None:
    layout = [
        [sg.Text("Enter the reader's username: "), sg.In(key="-NAME-")],
        [sg.HSeparator()],
        [sg.Text("Generating a new profile:")],
        [sg.Text("Enter the reader's username: "), sg.In(key="-NEW_NAME-")],
        [sg.Text(gender)],
        [sg.Text("Enter the corresponding number: "), sg.In(key="-GENDER-")],
        [sg.Text(age)],
        [sg.Text("Enter the corresponding number: "), sg.In(key="-AGE-")],
        [sg.Text(reading_style)],
        [sg.Text("Enter the corresponding number: "), sg.In(key="-READING_STYLE-")],
        [sg.Text(b.display_books(books))],
        [sg.Text("Enter the number of the books you've read, separated by comas (e.g. 5,7,10): "), sg.In(key="-BOOKS_READ-")],
        [sg.Button("Modify")]
    ]
    
    window = sg.Window("Modify reader", layout, finalize=True, modal=True)
    block_focus(window)
    
    event, values = window.read()
    
    reader_profile = [values["-NEW_NAME-"], values["-GENDER-"], values["-AGE-"], values["-READING_STYLE-"]]
    reader_booksread = [values["-NEW_NAME-"]] + values["-BOOKS_READ-"].split(",")
    
    if event == "Modify":
        re.reader_handling(books, readers, booksread, rating_matrix, reader_name=values["-NAME-"], reader_information=[reader_profile, reader_booksread], delete=False)
    
    window.close()
    
    
def delete_reader(books, readers: str, booksread: str, rating_matrix: list[list[int]]) -> None:
    layout = [
        [sg.Text("Enter the reader's username: "), sg.In(key="-NAME-")],
        [sg.Button("Delete")],
    ]
    
    window = sg.Window("Delete reader", layout, finalize=True, modal=True)
    block_focus(window)
    
    event, values = window.read()
    
    if event == "Delete":
        re.reader_handling(books, readers, booksread, rating_matrix, reader_name=values["-NAME-"], reader_information=None, delete=True)
        
    window.close()


def add_book(books: str, rating_matrix: list[list[int]]) -> None:
    layout = [
        [sg.Text(b.display_books(books))],
        [sg.Text("Enter the book's name: "), sg.In(key="-NAME-")],
        [sg.Button("Add")],
    ]
    
    window = sg.Window("Add book", layout, finalize=True, modal=True)
    block_focus(window)
    
    event, values = window.read()
    
    if event == "Add":
        b.add_books(books, rating_matrix, book_name=values["-NAME-"])
    
    window.close()
    
    
def modify_book(books: str, booksread: str, rating_matrix: list[list[int]]) -> None:
    layout = [
        [sg.Text(b.display_books(books))],
        [sg.Text("Enter the book's number: "), sg.In(key="-NAME-")],
        [sg.Text("Enter the book's new name: "), sg.In(key="-NEW_NAME-")],
        [sg.Button("Modify")],
    ]
    
    window = sg.Window("Modify book", layout, finalize=True, modal=True)
    block_focus(window)
    
    event, values = window.read()
    
    if event == "Modify":
        b.book_handling(books, booksread, rating_matrix, book_name=[values["-NAME-"], values["-NEW_NAME-"]], delete=False)
    
    window.close()
    
    
def delete_book(books: str, booksread: str, rating_matrix: list[list[int]]) -> None:
    layout = [
        [sg.Text(b.display_books(books))],
        [sg.Text("Enter the book's number: "), sg.In(key="-NAME-")],
        [sg.Button("Delete")]
    ]
    
    window = sg.Window("Delete book", layout, finalize=True, modal=True)
    block_focus(window)
    
    event, values = window.read()
    
    if event == "Delete":
        b.book_handling(books, booksread, rating_matrix, book_name=[values["-NAME-"]], delete=True)
    
    window.close()
    
    
def grade_book(books, rating_matrix: list[list[int]]) -> None:
    layout = [
        [sg.Text("Enter the reader's username: "), sg.In(key="-NAME-")],
        [sg.Text(b.display_books(books))],
        [sg.Text("Enter the book's number: "), sg.In(key="-BOOK-")],
        [sg.Text("Entrez the score (between 1 and 5): "), sg.In(key="-SCORE-")],
        [sg.Button("Grade")],
    ]
    
    window = sg.Window("Grade book", layout, finalize=True, modal=True)
    block_focus(window)
    
    event, values = window.read()
    
    if event == "Grade":
        info = [values["-NAME-"], values["-BOOK-"], values["-SCORE-"]]
        ra.grade_book(rating_matrix, info=info)
    
    window.close()
    
    
def recommend_book(books: str, booksread: str, rating_matrix: list[list[int]]) -> None:
    layout = [
        [sg.Text("Enter the reader's username: "), sg.In(key="-NAME-")],
        [sg.Button("Suggest")],
    ]
    
    window = sg.Window("Suggest book", layout, finalize=True, modal=True)
    block_focus(window)
    
    event, values = window.read()
    
    if event == "Suggest":
        sg.Popup(ra.recommend_book(books, booksread, rating_matrix, user_1=values["-NAME-"]))
    
    window.close()
    
    
def main(books: str, readers: str, booksread: str,
         rating_matrix: list[list[int]]) -> None:
    window = menu()
    block_focus(window)
    
    while True:
        event, values = window.read()
        
        if event in [sg.WINDOW_CLOSED, "Quit"]:
            break
        # Profils des readers
        elif event == "Add a reader":
            add_reader(books, readers, booksread, rating_matrix)
        elif event == "Display a reader":
            display_reader(books, readers, booksread)
        elif event == "Modify a reader":
            modify_reader(books, readers, booksread, rating_matrix)
        elif event == "Delete a reader":
            delete_reader(books, readers, booksread, rating_matrix)
            
        # Visiter le dépôt des books
        elif event == "Display book":
            sg.Popup(b.display_books(books))
        elif event == "Add a book":
            add_book(books, rating_matrix)
        elif event == "Modify a book":
            modify_book(books, booksread, rating_matrix)
        elif event == "Delete a book":
            delete_book(books, booksread, rating_matrix)
        
        # Recommendation
        elif event == "Grade a book":
            grade_book(readers, rating_matrix)
        elif event == "Recommend a book":
            recommend_book(books, booksread, rating_matrix)
    
    window.close()