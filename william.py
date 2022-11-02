import os
import csv
os.system("cls")

from libro import *

def cargaLibros():
    with open("books.csv", "r", encoding='utf-8') as f:
        archivo = csv.DictReader(f)
        libros = []
        for row in archivo:
            libros.append(row)
    return libros


def listarLibros(libros):
    listaLibros = []
    for atributo in libros:
        _id = atributo["id"]
        title = atributo["title"]
        genre = atributo["genre"]
        ISBN = atributo["ISBN"]
        editorial = atributo["editorial"]
        authors = atributo["authors"].split(";")
        libro = Libro(_id, title, genre, ISBN, editorial, authors)
        listaLibros.append(libro)

    for libro in listaLibros:
        libro.mostrarLibro()
        print()

def opcion01():
    librosCargar = int(
        input("\n¿Cuántos libros desea cargar? Ingrese un número: "))
    with open("books.csv", "r", encoding='utf-8') as f:
        archivo = csv.DictReader(f)
        libros = []
        libronumero = 0
        for row in archivo:
            if libronumero == librosCargar:
                break
            libros.append(row)
            libronumero += 1
    print()
    listarLibros(libros)
    print("Carga completa")
    # return libros


def opcion02():
    print("\nContamos con los siguientes libros...\n")
    libros = cargaLibros()
    listarLibros(libros)
    print("Carga completa")
    # return libros

def opcion03():
    print("\nAgregando un nuevo libro...\n")
    libros = cargaLibros()
    _id = input("Ingrese el id: ")
    title = input("Ingrese el título: ")
    genre = input("Ingrese el género: ")
    ISBN = input("Ingrese el ISBN: ")
    editorial = input("Ingrese la editorial: ")
    authors = input("Ingrese el autor o los autores (separados mediante ;): ")
    libro = Libro(_id, title, genre, ISBN, editorial, authors)
    libro.registro()
    # libros.append(libro.get_book())
    with open("books.csv", "a", encoding="utf-8", newline="\n") as f_write:
        campos = ["id","title","genre","ISBN","editorial","authors"]
        registro = csv.DictWriter(f_write,fieldnames=campos)
        registro.writerow(libro.get_book())
    print("\nSe agregó un libro")
    # return libros

def opcion04():
    print("\nEliminando un libro...\n")
    with open("books.csv", "r", encoding='utf-8') as f:
        file = csv.DictReader(f)
        books = []
        for row in file:
            books.append(row)

    idDisponible = [book["id"] for book in books]

    while True:
        delete = input("Ingrese el ID del libro a borrar: ")
        if delete in idDisponible:
            indice = idDisponible.index(delete)
            break
        else:
            print("Ingrese un ID válido")

    books.pop(indice)

    with open("books.csv", "w", encoding="utf-8", newline="\n") as f_write:
        campos = ["id","title","genre","ISBN","editorial","authors"]
        registro = csv.DictWriter(f_write,fieldnames=campos)
        registro.writeheader()
        registro.writerows(books[:])

    print("\nSe eliminó el libro")

opciones = ["opcion01()", "opcion02()", "opcion03()","opcion04()","opcion05()","opcion06()","opcion07()","opcion08()","opcion09()","opcion10()"]

def mostrarOpciones():
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
    mostrarOpciones()
    opcion = int(input("Ingrese el número de la opción: "))
    eval(opciones[opcion-1])
    print("----------------------------------------------")
    continuar = input("¿Desea elegir otra opción? S/N: ").upper()
    if continuar == "S":
        print()
        continue
    else:
        break