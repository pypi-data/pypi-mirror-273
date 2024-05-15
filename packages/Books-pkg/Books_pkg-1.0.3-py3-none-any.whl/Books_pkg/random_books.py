import pkg_resources
import pandas as pd

class RandomBooks:
    FILE_PATH = pkg_resources.resource_filename(__name__,'books.csv')

    def __init__(self):
        self._file = pd.read_csv(RandomBooks.FILE_PATH)
        self._books = None
        self._title = None
        self._author = None
        self._genre = None
        self._height = None
        self._publisher = None

    def generate_random(self):
        self._books = self._file.sample()
        self._title = self._books["Title"].values[0]
        self._author = self._books["Author"].values[0]
        self._genre = self._books["Genre"].values[0]
        self._height = self._books["#"].values[0]
        self._publisher = self._books["Publisher"].values[0]

    def buscar_title(title):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Title"] == title]
        if buscar.size == 0:
            return "No se encontro el Titulo: "
        else:
            return buscar

    def buscar_author(author):
        file = "books.csv"
        datos = pd.read_csv(file)
        buscar = datos[datos["Author"] == author]
        if buscar.size == 0:
            return "No se encontro el Titulo: "
        else:
            return buscar

