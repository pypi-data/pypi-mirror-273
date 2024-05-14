import pkg_resources
import pandas as pd

class SelectBooks:
    FILE_PATH = pkg_resources.resource_filename(__name__,'books.csv')

    def __init__(self):
        self._file = pd.read_csv(SelectBooks.FILE_PATH)
        self._number = None
        self._title = None
        self._author = None
        self._genre = None
        self._height = None
        self._publisher = None

    def generate_random(self):
        self._books = self._file.saple()
        self._number = self._books["#"].values[0]
        self._title = self._books["Title"].values[0]
        self._author = self._books["Author"].values[0]
        self._genre = self._books["Genre"].values[0]
        self._height = self._books["Height"].values[0]
        self._publisher = self._books["Publisher"].values[0]

    def buscar_Number(_number):
        buscar = ["Title"] == _number
        if buscar == 0:
            return "No se encontro el titulo "
        else:
            return buscar

    def buscar_Title(_title):
        buscar = ["Title"] == _title
        if buscar == 0:
            return "No se encontro el titulo "
        else:
            return buscar


    def buscar_Author(_author):
        buscar = ["Author"] == _author
        if buscar == 0:
            return "No se encontro el autor"
        else:
            return buscar


