#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse

from core import rating as ra
import menu_cli


def main() -> None:
    parser = argparse.ArgumentParser(description="Recommend a book based on what you have read.")
    parser.add_argument("--type", help="Choose between cli or gui version.")
    args = parser.parse_args()
    
    books = "docs/books.txt"
    readers = "docs/readers.txt"
    booksread = "docs/booksread.txt"
    matrix = "docs/rating_matrix.txt"
    rating_matrix = ra.get_matrix(matrix)
    
    if args.type == "gui":
        pass
    else:
        menu_cli.main_menu(books, readers, booksread, rating_matrix)
        
        
if __name__ == "__main__":
    main()