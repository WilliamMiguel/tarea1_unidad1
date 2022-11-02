class Libro():
    def __init__(self, id: int , titulo: str, genero: str, isbn: str, editorial: str, autor: str) -> None:
        self.__id = id
        self.__titulo = titulo
        self.__genero = genero
        self.__isbn = isbn
        self.__editorial = editorial
        self.__autor = autor

    def set_id(self, id: int) -> None:
        self.__id = id
    
    def get_id(self) -> int:
        return self.__id 

    def set_titulo(self, titulo: str) -> None:
        self.__titulo = titulo
    
    def get_titulo(self) -> str:
        return self.__titulo 

    def set_genero(self, genero: str) -> None:
        self.__genero = genero
    
    def get_genero(self) -> str:
        return self.__genero 

    def set_isbn(self, isbn: str) -> None:
        self.__isbn = isbn
    
    def get_isbn(self) -> str:
        return self.__isbn

    def set_editorial(self, editorial: str) -> None:
        self.__editorial = editorial
    
    def get_editorial(self) -> str:
        return self.__editorial 

    def set_autor(self, autor: str) -> None:
        self.__autor = autor
    
    def get_autor(self) -> str:
        return self.__autor
