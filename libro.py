class Libro:
    def __init__(self, _id: int , title: str, genre: str, isbn: str, editorial: str, authors: str) -> None:
        self.__id = _id
        self.__title = title
        self.__genre = genre
        self.__isbn = isbn
        self.__editorial = editorial
        self.__authors = authors
        self.__book = {}

    def set_id(self, _id: int) -> None:
        self.__id = _id
    
    def get_id(self) -> int:
        return self.__id 

    def set_title(self, title: str) -> None:
        self.__title = title
    
    def get_title(self) -> str:
        return self.__title

    def set_genre(self, genre: str) -> None:
        self.__genre = genre
    
    def get_genero(self) -> str:
        return self.__genre

    def set_isbn(self, isbn: str) -> None:
        self.__isbn = isbn
    
    def get_isbn(self) -> str:
        return self.__isbn

    def set_editorial(self, editorial: str) -> None:
        self.__editorial = editorial
    
    def get_editorial(self) -> str:
        return self.__editorial 

    def set_autor(self, authors: str) -> None:
        self.__authors = authors
    
    def get_autor(self) -> str:
        return self.__authors

    def registro(self):
        self.__book["id"] = self.__id
        self.__book["title"] = self.__title
        self.__book["genre"] = self.__genre
        self.__book["ISBN"] = self.__isbn
        self.__book["editorial"] = self.__editorial
        self.__book["authors"] = self.__authors

    def get_book(self):
        return self.__book

    def showBook(self):
        print(f"Título: {self.__title}")
        print(f"Género: {self.__genre}")
        print(f"ISBN: {self.__isbn}")
        print(f"Editorial: {self.__editorial}")
        print("Autor(es):")
        print(*self.__authors, sep=", ")