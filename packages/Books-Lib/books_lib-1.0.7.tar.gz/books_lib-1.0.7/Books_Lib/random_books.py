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
        self._books = self._file.saple()
        self._number = self._books["#"].values[0]
        self._title = self._books["Title"].values[0]
        self._author = self._books["Author"].values[0]
        self._genre = self._books["Genre"].values[0]
        self._height = self._books["Height"].values[0]
        self._publisher = self._books["Publisher"].values[0]

    def buscar_Number(_number):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Number"] == _number]
        if buscar.size == 0:
            return "No se encontro el titulo "
        else:
            return buscar

    def buscar_Title(_title):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Title"] == _title]
        if buscar.size == 0:
            return "No se encontro el titulo "
        else:
            return buscar


    def buscar_Author(_author):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Author"] == _author]
        if buscar.size == 0:
            return "No se encontro el autor"
        else:
            return buscar

    def buscar_Genre(_genre):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Genre"] == _genre]
        if buscar.size == 0:
            return "No se encontro el autor"
        else:
            return buscar


    def buscar_Height(_height):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Height"] == _height]
        if buscar.size == 0:
            return "No se encontro el autor"
        else:
            return buscar

    def buscar_Publisher(_publisher):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Publisher"] == _publisher]
        if buscar.size == 0:
            return "No se encontro el autor"
        else:
            return buscar

