from libro import *
from tabulate import tabulate
import os
import csv

def loadBooks():
    with open("books.csv", "r", encoding='utf-8') as f:
        file = csv.DictReader(f)
        books = []
        for row in file:
            books.append(row)
    return books

# def listBooks(books):
#     listofBooks = []
#     for attribute in books:
#         _id = attribute["id"]
#         title = attribute["title"]
#         genre = attribute["genre"]
#         isbn = attribute["ISBN"]
#         editorial = attribute["editorial"]
#         authors = attribute["authors"].split(";")
#         book = Libro(_id, title, genre, isbn, editorial, authors)
#         listofBooks.append(book)

#     for book in listofBooks:
#         book.showBook()
#         print()

def tableBooks(books):
    ids = [book["id"] for book in books]
    titles = [book["title"] for book in books]
    genre = [book["genre"] for book in books]
    isbn = [book["ISBN"] for book in books]
    editorial = [book["editorial"] for book in books]
    authors = [book["authors"] for book in books]

    tupleBooks = zip(ids, titles, genre, isbn, editorial, authors)
    fieldnames = ["ID", "Título", "Género", "ISBN", "Editorial", "Autor(es)"]
    print(tabulate(tupleBooks, headers=fieldnames))
    print()

def isEmpty(texto):
    while True:
        attribute = input(texto).strip()
        if len(attribute) != 0:
            break
    return attribute

def option01():
    print()
    while True:
        upBooks = input("¿Cuántos libros desea cargar? Ingrese un número: ")
        if upBooks.isnumeric():
            break

    with open("books.csv", "r", encoding='utf-8') as f:
        file = csv.DictReader(f)
        books = []
        bookNumber = 0
        for row in file:
            if bookNumber == int(upBooks):
                break
            books.append(row)
            bookNumber += 1
        
    print("\nCARGANDO LIBROS...\n")
    tableBooks(books)
    if bookNumber < int(upBooks):
        print(f"ENCONTRAMOS {bookNumber} LIBROS")
    else:
        print("CARGA COMPLETA")

def option02():
    print("\nCONTAMOS CON LOS SIGUIENTES LIBROS...\n")
    books = loadBooks()
    tableBooks(books)
    print("Carga completa")


def option03():
    print("\nAGREGANDO UN LIBRO...\n")
    _id = isEmpty("Ingrese el ID: ")
    title = isEmpty("Ingrese el título: ")
    genre = isEmpty("Ingrese el género: ")
    ISBN = isEmpty("Ingrese el ISBN: ")
    editorial = isEmpty("Ingrese la editorial: ")
    authors = isEmpty(
        "Ingrese el autor o los autores (separados mediante ;): ")
    book = Libro(_id, title, genre, ISBN, editorial, authors)
    book.registro()
    with open("books.csv", "a", encoding="utf-8", newline="\n") as f_write:
        fieldnames = ["id", "title", "genre", "ISBN", "editorial", "authors"]
        register = csv.DictWriter(f_write, fieldnames=fieldnames)
        register.writerow(book.get_book())
    print("\nSe agregó un libro")


def option04():
    print("\nELIMINANDO UN LIBRO...\n")
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
        fieldnames = ["id", "title", "genre", "ISBN", "editorial", "authors"]
        register = csv.DictWriter(f_write, fieldnames=fieldnames)
        register.writeheader()
        register.writerows(books[:])

    print("\nSe eliminó el libro")


options = ["option01()", "option02()", "option03()", "option04()", "option05()",
           "option06()", "option07()", "option08()", "option09()", "option10()"]


def showOptions():
    print("Elije una de las siguientes opciones:")
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


optionsNumber = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]



while True:
    os.system("cls")
    print("\t\tBIENVENIDO(A) A NUESTRA BIBLIOTECA\n")
    showOptions()
    while True:
        option = input("Ingrese el número de una opción: ")
        if option in optionsNumber:
            break
    eval(options[int(option)-1])
    print("----------------------------------------------")
    while True:
        proceed = input("¿Desea elegir otra opción? S/N: ").upper()
        if proceed == "S" or proceed == "N":
            break

    if proceed == "S":
        print()
        continue
    else:
        break
