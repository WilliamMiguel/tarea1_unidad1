import os
import csv
os.system("cls")

from libro import *

def loadBooks():
    with open("books.csv", "r", encoding='utf-8') as f:
        file = csv.DictReader(f)
        books = []
        for row in file:
            books.append(row)
    return books

def listBooks(books):
    listofBooks = []
    for attribute in books:
        _id = attribute["id"]
        title = attribute["title"]
        genre = attribute["genre"]
        isbn = attribute["ISBN"]
        editorial = attribute["editorial"]
        authors = attribute["authors"].split(";")
        book = Libro(_id, title, genre, isbn, editorial, authors)
        listofBooks.append(book)

    for book in listofBooks:
        book.showBook()
        print()

def option01():
    upBooks = int(input("\n¿Cuántos libros desea cargar? Ingrese un número: "))
    with open("books.csv", "r", encoding='utf-8') as f:
        file = csv.DictReader(f)
        books = []
        bookNumber = 0
        for row in file:
            if bookNumber == upBooks:
                break
            books.append(row)
            bookNumber += 1
    print()
    listBooks(books)
    print("Carga completa")

def option02():
    print("\nContamos con los siguientes libros...\n")
    books = loadBooks()
    listBooks(books)
    print("Carga completa")

def option03():
    print("\nAgregando un nuevo libro...\n")
    _id = input("Ingrese el id: ")
    title = input("Ingrese el título: ")
    genre = input("Ingrese el género: ")
    ISBN = input("Ingrese el ISBN: ")
    editorial = input("Ingrese la editorial: ")
    authors = input("Ingrese el autor o los autores (separados mediante ;): ")
    book = Libro(_id, title, genre, ISBN, editorial, authors)
    book.registro()
    with open("books.csv", "a", encoding="utf-8", newline="\n") as f_write:
        fieldnames = ["id","title","genre","ISBN","editorial","authors"]
        register = csv.DictWriter(f_write, fieldnames = fieldnames)
        register.writerow(book.get_book())
    print("\nSe agregó un libro")

def option04():
    print("\nEliminando un libro...\n")
    with open("books.csv", "r", encoding='utf-8') as f:
        file = csv.DictReader(f)
        books = []
        for row in file:
            books.append(row)

    idAvailable = [book["id"] for book in books]

    while True:
        delete = input("Ingrese el ID del libro a borrar: ")
        if delete in idAvailable:
            index = idAvailable.index(delete)
            break
        else:
            print("Ingrese un ID válido")

    books.pop(index)

    with open("books.csv", "w", encoding="utf-8", newline="\n") as f_write:
        fieldnames = ["id","title","genre","ISBN","editorial","authors"]
        register = csv.DictWriter(f_write, fieldnames = fieldnames)
        register.writeheader()
        register.writerows(books[:])

    print("\nSe eliminó el libro")

options = ["option01()", "option02()", "option03()","option04()","option05()","option06()","option07()","option08()","option09()","option10()"]

def showOptions():
    print("Elija una de las siguientes opciones:")
    print('''    Opción 1: Leer archivo de disco duro (.txt o csv).
    Opción 2: Listar libros.
    Opción 3: Agregar libro.
    Opción 4: Eliminar libro.
    Opción 5: Buscar libro por ISBN o por título.
    Opción 6: Ordenar libros por título.
    Opción 7: Buscar libros por autor, editorial o género.
    Opción 8: Buscar libros por número de autores.
    Opción 9: Editar o actualizar datos de un libro (título, género, ISBN, editorial y autores).
    Opción 10: Guardar libros en archivo de disco duro (.txt o csv).
    ''')

while True:
    showOptions()
    option = int(input("Ingrese el número de la opción: "))
    eval(options[option-1])
    print("----------------------------------------------")
    proceed = input("¿Desea elegir otra opción? S/N: ").upper()
    if proceed == "S":
        print()
        continue
    else:
        break
    
    