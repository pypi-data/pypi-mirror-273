import pkg_resources
import pandas as pd

class SelectBooks:
    FILE_PATH = pkg_resources.resource_filename(__name__,'books.csv')

    def __init__(self):
        self._file = pd.read_csv(SelectBooks.FILE_PATH)
        self._title = None
        self._author = None
        self._genre = None
        self._height = None
        self._publisher = None

    def generate_books(self):
        self._books = self._file.sample()
        self._title = self._books["Title"].values[0]
        self._author = self._books["Author"].values[0]
        self._genre = self._books["Genre"].values[0]
        self._height = self._books["Height"].values[0]
        self._publisher = self._books["Publisher"].values[0]


    def buscar_Title(title):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar =datos[ datos["Title"] == title]
        if buscar.size == 0:
            return "No se encontro el titulo "
        else:
            return buscar

    def buscar_Author(author):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Author"] == author]
        if buscar.size == 0:
            return "No se encontro el autor"
        else:
            return buscar


    def getBooks(self):
        return self._books

    def getTitle(self):
        return self._title

    def getAuth(self):
        return self._author

    def getGenre(self):
        return self._genre

    def getHeig(self):
        return self._height

    def getPubli(self):
        return self._publisher


