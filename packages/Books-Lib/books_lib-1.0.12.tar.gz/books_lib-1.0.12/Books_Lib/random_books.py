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

    def getAuthor(self):
        return self._author
    def getTitle(self):
        return self._title
    def getGenre(self):
        return self._genre
    def getHeight(self):
        return self._height
    def getPublisher(self):
        return self._publisher



