#-------------------------------------------- Importaciones --------------------------------------------
from libro import *
import os
import csv

#os.system("pip install tabulate")
#os.system("pip install colorama")

from tabulate import tabulate
from colorama import init,Back,Fore,Style

init(autoreset = True)

#-------------------------------------------- Cargar Libros --------------------------------------------
def loadBooks() -> list[dict]:
    with open("books.csv", "r", encoding='utf-8') as f:
        file: csv.DictReader[str] = csv.DictReader(f)
        books: list[dict] = []

        for row in file:
            books.append(row)
    return books

#-------------------------------------------- Imprimir Libros En Tabla --------------------------------------------
def tableBooks(books: list[dict]) -> None:
    ids:list[str] = [book["id"] for book in books]
    titles:list[str] = [book["title"] for book in books]
    genre:list[str] = [book["genre"] for book in books]
    isbn:list[str] = [book["isbn"] for book in books]
    editorial:list[str] = [book["editorial"] for book in books]
    authors:list[str] = [book["authors"] for book in books]
    tupleBooks:zip[tuple] = zip(ids, titles, genre, isbn, editorial, authors)
    fieldnames:list[str]= ["ID", "Título", "Género", "ISBN", "Editorial", "Autor(es)"]

    print(tabulate(tupleBooks, headers=fieldnames))
    print()

#-------------------------------------------- Función Para Validar Id Ingresado --------------------------------------------
def validateId(id: str, books: list[str], messageInvalidId: str) -> str:
    ids:list[str] = [book["id"] for book in books]

    while True:
        if id not in ids:
            id = input(Fore.RED + messageInvalidId)
            continue
        break

    return id

#-------------------------------------------- Valida Si La Cadena Está Vacía --------------------------------------------
def isEmpty(texto: str) -> str:
    while True:
        attribute:str = input(texto).strip()

        if len(attribute) != 0:
            break
    return attribute

#-------------------------------------------- Opción 01 --------------------------------------------
def option01(books:list[dict]) -> list[dict]:
    print()
    while True:
        upBooks: str = input("¿Cuántos libros desea cargar? Ingrese un número: ")
        if upBooks.isnumeric():
            break

    newBooks: list[dict] = []
    bookNumber: int = 0

    for book in books:
        if bookNumber == int(upBooks):
            break

        newBooks.append(book)
        bookNumber += 1

    print("\nCARGANDO LIBROS...\n")

    if bookNumber < int(upBooks):
        print(Fore.YELLOW + f"ENCONTRAMOS {bookNumber} LIBROS\n")
    else:
        print(Fore.GREEN + "CARGA COMPLETA\n")

    return newBooks

#-------------------------------------------- Opción 02 --------------------------------------------
def option02(books: list[dict]) -> None:
    print(Fore.LIGHTBLUE_EX + "\nCONTAMOS CON LOS SIGUIENTES LIBROS...\n")
    tableBooks(books)
    print(Fore.GREEN + "Carga completa\n")

#-------------------------------------------- Opción 03 --------------------------------------------
def option03(idsAll: list[str], books: list[dict]) -> list[dict]:
    print("\nAGREGANDO UN LIBRO...\n")
    
    # Combinamos los ids de todos los libros
    setIds =  set(idsAll + [book["id"] for book in books])

    id: str = isEmpty("Ingrese el ID: ")

    while True: 
        if (id in setIds):
            id = input(Fore.RED+"El id ya se encuentra registrado. Ingrese nuevamente el ID: " + Fore.RESET)
            continue
        break
    
    title: str = isEmpty("\nIngrese el título: ")
    genre: str = isEmpty("Ingrese el género: ")
    isbn: str = isEmpty("Ingrese el ISBN: ")
    editorial: str = isEmpty("Ingrese la editorial: ")
    authors: str = isEmpty("Ingrese el autor o los autores (separados mediante ;): ")
   
    book: Libro = Libro(id, title, genre, isbn, editorial, authors)
    book.registro()
    books.append(book.get_book())

    print(Fore.GREEN+"\nSe agregó un libro\n")
    return books

#-------------------------------------------- Opción 04 --------------------------------------------
def option04(books: list[dict]) -> list[dict]:
    print(Fore.RED+"\nEliminando libro\n")

    id: str = input("Ingrese el id del libro a eliminar: ")

    id = validateId(id, books, "Id inválido. Ingresa nuevamente el id del libro a eliminar: " + Fore.RESET)

    def filterListBooks(book: dict):
        if book["id"] != id: return book
    
    newListBooks: list[dict] =  list(filter(filterListBooks , books))

    print(Fore.RED+f"\nSe eliminó el libro con el id: {id}\n")

    return newListBooks 

#-------------------------------------------- Opción 05 Y Opción 07 --------------------------------------------
def option05or07(optionType: int, books: list[dict]) -> None:
    print("\nElije la opción de búsqueda Ejemp(1):")

    isOption05: bool = optionType == 1
    listOptions: list[str] = []

    if (isOption05):
        print('''    Opcion 1: Buscar libro por ISBN.
    Opción 2: Buscar libro por título.
        ''')
        listOptions = ["1", "2"]
    else: 
        print('''    Opcion 1: Buscar libro por autor.
    Opción 2: Buscar libro por editorial.
    Opción 3: Buscar libro por género.
        ''')
        listOptions = ["1", "2", "3"]

    search: str = ""
    while (True):
        if (search not in listOptions):
            search = input(Fore.GREEN+"Ingrese la opción de búsqueda: ")
            continue
        break

    print()

    text: str = ""
    while (True): 
        if (text == "" or text.isspace()):
            if (search == "1"): 
                if(isOption05) :
                    text = input("Ingrese el ISBN a buscar: ")
                else:
                    text = input("Ingrese el autor a buscar: ")
                continue
            if (search == "2"):
                if (isOption05) : 
                    text = input("Ingrese el título a buscar: ")
                else : 
                    text = input("Ingrese el editorial a buscar: ")
                continue
            if (search == "3"):
                text = input("Ingrese el género a buscar: ")
                continue
        break
    
    print()

    searchFilter: str = ""
    if (search == "1") : 
        if (isOption05) : searchFilter = "isbn"
        else : searchFilter = "authors"
    if (search == "2") : 
        if (isOption05) : searchFilter = "title"
        else : searchFilter = "editorial"
    if (search == "3"): searchFilter = "genre"

    listBookFilter: list[dict] = list(filter((lambda book: text in book[searchFilter]), books))

    tableBooks(listBookFilter)
    print()

#-------------------------------------------- Opción 06 --------------------------------------------
def option06(books: list[dict]) -> None:
    print()
    listBookOrdered: list[dict] = list(sorted(books, key = lambda book : book["title"]))
    tableBooks(listBookOrdered)

#-------------------------------------------- Opción 08 --------------------------------------------
def option08(books: list[dict]) -> None:
    numberAuthors: str = ""
    while (True) :
        if (not(numberAuthors.isnumeric())) :
            numberAuthors = input(Fore.GREEN+"\nIngrese el número de autores: ")
            continue
        
        numberAuthors: int = int(numberAuthors)
        break
    
    def filterByNumbersAuthors(book: dict) -> bool:
        listAuthors: list[str] = book["authors"].split(";")
        return len(listAuthors) == numberAuthors

    listBookByNumbersAuthors: list[dict] = list(filter(filterByNumbersAuthors, books))
    
    print()
    tableBooks(listBookByNumbersAuthors)

#-------------------------------------------- Opción 09 --------------------------------------------
def option09(books: list[dict]) -> list[dict]:
    print(Fore.GREEN+"\nActualizando libro\n")

    id:str = input("Ingrese el id del libro a modificar: ")

    id = validateId(id, books, Fore.RED + "Id inválido. Ingresa nuevamente el id del libro a actualizar: " + Fore.RESET)

    title:str = input("\nIngrese el título: ")
    genre:str = input("Ingrese el género: ")
    isbn:str = input("Ingrese el ISBN: ")
    editorial:str = input("Ingrese la editorial: ")
    authors:str = input("Ingrese el autor o los autores (separados mediante ;): ")

    def mapListBooks(book: dict) -> dict:
        if book["id"] == id:
            book["title"] = title
            book["genre"] = genre
            book["isbn"] = isbn
            book["editorial"] = editorial
            book["authors"] = authors
        return book
    
    newListBooks: list[dict] =  list(map(mapListBooks , books))

    print(Fore.GREEN + f"\nSe actualizó el libro con el id: {id}\n")

    return newListBooks 

#-------------------------------------------- Opción 10 --------------------------------------------
def option10(books: list[dict]):
    with open("books.csv", "w", encoding="utf-8", newline="\n") as f_write:
        fieldnames: list[str] = ["id", "title", "genre", "isbn", "editorial", "authors"]

        register: csv.DictWriter[str] = csv.DictWriter(f_write, fieldnames=fieldnames)
        register.writeheader()
        register.writerows(books[:])
    
    print(Fore.BLUE + "\nCAMBIOS GUARDADOS\n")

def option10additional():
        newBooks: list[dict] = []
        booksSelectedForExtract: list[dict] = booksSelected
        
        # ----------------------------------- Para El Eliminado y Actualización -----------------------------------
        # Recorriendo todos los libros
        for book in booksAll:
            if (book["id"] not in idsSelected): 
                newBooks.append(book)
                continue

            # Recorriendo todos los libros seleccionados
            for bookSe in booksSelected:
                # En caso de que se haya actualizado se agregará el libro seleccionado en la nueva lista
                if (book["id"] == bookSe["id"]):
                    newBooks.append(bookSe)
                    booksSelectedForExtract.remove(bookSe)
                    break 

        # ----------------------------------- Para La Inserción -----------------------------------
        for book in booksSelectedForExtract:
            newBooks.append(book)

        option10(newBooks)

#-------------------------------------------- Función de Elegir Otras Opciones --------------------------------------------
def showOtherOptions(saveChanges: int):
    while True:
        proceed: str = input(Fore.MAGENTA + "¿Desea elegir otra opción? S/N: ").upper()
        if proceed == "S" or proceed == "N":
            break

    if proceed == "S":
        print()

    if proceed == "N" and saveChanges == 0:
        while True:
            saveChanges: str = input("\nNo has guardado los cambios. ¿Salir sin guardar? S/N: ").upper()
            if saveChanges == "S":
                quit()
            elif saveChanges == "N":
                option10additional()
                quit()

#-------------------------------------------- Ejecución Del Programa --------------------------------------------
def showOptions():
    print(Fore.BLUE+"Elije una de las siguientes opciones:")
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

optionsNumber: list[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

booksAll: list[dict] = loadBooks()
booksSelected: list[dict] = []
# Variable que decidirá si hubo una eliminación o un agregado
idsSelected:list[str] = []
# Variable que nos servirá para validar que no haya id repetidos
idsAll: list[str] =  [book["id"] for book in booksAll]

while True:
    os.system("cls")
    print(Back.CYAN + "BIENVENIDO(A) A NUESTRA BIBLIOTECA\n")
    showOptions()

    while True:
        option: str = input(Fore.BLUE+"Ingrese el número de una opción: ")
        
        if option in optionsNumber:
            option: int = int(option)
            break

    saveChanges: int = 0

    if (option in range(2, 11, 1) and not booksSelected and not idsSelected):
        print("\nNo cargaste ningún libro\n")

        backTo = input("Presiona Enter para regresar a las opciones o cualquier tecla para salir... ")

        if backTo == " " or backTo.isalpha() or backTo.isnumeric():
            quit()
        else:
            continue

    if ((option == 4 or option == 9) and not booksSelected and idsSelected):
        if (option == 4):
            print("\nNo hay ningún libro para eliminar\n")
            
        if (option == 9):
            print("\nNo hay ningún libro para actualizar\n")
        
        showOtherOptions(saveChanges)
        continue
        
    if option == 1:
        booksAll = loadBooks()
        booksSelected = option01(booksAll)
        idsSelected = [book["id"] for book in booksSelected]
    if option == 2:
        option02(booksSelected)
    if option == 3:
        booksSelected = option03(idsAll, booksSelected)
    if option == 4:
        booksSelected = option04(booksSelected)
    if option == 5:
        option05or07(1, booksSelected)
    if option == 6:
        option06(booksSelected)
    if option == 7:
        option05or07(2, booksSelected)
    if option == 8:
        option08(booksSelected)
    if option == 9:
        booksSelected = option09(booksSelected)
    if option == 10:
        saveChanges = 1
        option10additional()

    print("----------------------------------------------")

    showOtherOptions(saveChanges)
