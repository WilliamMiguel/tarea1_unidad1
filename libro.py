class Libro:
    def __init__(self, id: str , title: str, genre: str, isbn: str, editorial: str, authors: str) -> None:
        self.__id = id
        self.__title = title
        self.__genre = genre
        self.__isbn = isbn
        self.__editorial = editorial
        self.__authors = authors
        self.__book = {}

    def set_id(self, id: str) -> None:
        self.__id = id
    
    def get_id(self) -> str:
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

    def registro(self) -> None:
        self.__book["id"] = self.__id
        self.__book["title"] = self.__title
        self.__book["genre"] = self.__genre
        self.__book["isbn"] = self.__isbn
        self.__book["editorial"] = self.__editorial
        self.__book["authors"] = self.__authors

    def get_book(self) -> dict:
        return self.__book